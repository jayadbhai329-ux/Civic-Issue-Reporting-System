import io
import random
import string
import os
import mysql.connector
from mysql.connector import Error, IntegrityError
from functools import wraps
from datetime import datetime

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory,
    jsonify,
    send_file,
    make_response,
    abort
)

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw, ImageFont

from ai_detector import validate_civic_complaint, detect_civic_issue, compute_dhash


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

# MySQL configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "civic_issues_db",
    "port": 3306
}


app = Flask(__name__)

app.secret_key = "change-this-secret-key-before-deployment"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    conn = get_db()
    cursor = conn.cursor()

    try:

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                phone VARCHAR(50),
                password VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL DEFAULT 'citizen',
                created_at DATETIME NOT NULL
            )
        """)

        # Issues table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                title VARCHAR(255) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT NOT NULL,
                location VARCHAR(255) NOT NULL,
                image VARCHAR(255),
                status VARCHAR(50) NOT NULL DEFAULT 'Pending',
                admin_note TEXT,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
                ON DELETE CASCADE
            )
        """)

        # Ensure AI validation columns exist in issues table
        cursor.execute("SHOW COLUMNS FROM issues")
        existing_cols = {c[0] for c in cursor.fetchall()}
        new_cols = [
            ("validation_status", "VARCHAR(50) DEFAULT 'PENDING'"),
            ("predicted_category", "VARCHAR(100)"),
            ("ai_confidence", "FLOAT"),
            ("review_decision", "VARCHAR(50)"),
            ("image_phash", "VARCHAR(64)"),
            ("ai_explanation", "TEXT")
        ]
        for col_name, col_type in new_cols:
            if col_name not in existing_cols:
                cursor.execute(f"ALTER TABLE issues ADD COLUMN {col_name} {col_type}")

        # Check if admin exists
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            ("admin@civic.local",)
        )


        admin = cursor.fetchone()

        # Create default admin
        if not admin:

            cursor.execute(
                """
                INSERT INTO users
                (name, email, phone, password, role, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    "System Administrator",
                    "admin@civic.local",
                    "",
                    generate_password_hash("admin123"),
                    "admin",
                    datetime.now()
                )
            )

        conn.commit()

    finally:
        cursor.close()
        conn.close()


# ============================================================
# LOGIN REQUIRED
# ============================================================

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if "user_id" not in session:
            flash("Please login to continue.", "warning")
            next_url = request.full_path if request.query_string else request.path
            return redirect(url_for("login", next=next_url))

        return f(*args, **kwargs)

    return decorated


# ============================================================
# ADMIN REQUIRED
# ============================================================

def admin_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if session.get("role") != "admin":
            flash("Admin access required.", "danger")
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated


# ============================================================
# FILE VALIDATION
# ============================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# ============================================================
# CURRENT USER
# ============================================================

@app.context_processor
def inject_user():

    return {
        "current_user": session.get("name")
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def index():

    return render_template("index.html")


# ============================================================
# CAPTCHA GENERATION
# ============================================================

def generate_captcha_text(length=5):
    # Characters omitting easily confused glyphs (0, O, 1, I)
    charset = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    return "".join(random.choice(charset) for _ in range(length))


def create_captcha_image(text):
    w, h = 180, 52
    img = Image.new("RGB", (w, h), color=(245, 248, 252))
    draw = ImageDraw.Draw(img)

    # Background noise dots
    for _ in range(80):
        xy = (random.randint(0, w), random.randint(0, h))
        draw.point(xy, fill=(random.randint(180, 220), random.randint(190, 230), random.randint(200, 240)))

    # Interference curve lines
    for _ in range(3):
        start = (random.randint(0, 30), random.randint(10, h - 10))
        ctrl = (random.randint(40, w - 40), random.randint(5, h - 5))
        end = (random.randint(w - 30, w), random.randint(10, h - 10))
        draw.line([start, ctrl, end], fill=(random.randint(160, 205), random.randint(180, 225), random.randint(210, 245)), width=2)

    try:
        font = ImageFont.truetype("arial.ttf", 30)
    except Exception:
        font = ImageFont.load_default()

    char_w = w // (len(text) + 1)
    colors = [(16, 42, 92), (22, 119, 242), (3, 105, 161), (30, 64, 175), (15, 23, 42)]
    for i, ch in enumerate(text):
        c_img = Image.new("RGBA", (38, 46), (255, 255, 255, 0))
        c_draw = ImageDraw.Draw(c_img)
        c_draw.text((4, 2), ch, font=font, fill=random.choice(colors))
        angle = random.randint(-18, 18)
        c_rot = c_img.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
        pos = (14 + i * char_w, random.randint(4, 9))
        img.paste(c_rot, pos, c_rot)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


@app.route("/captcha/<form_type>")
def captcha_image(form_type):
    if form_type not in ["login", "register"]:
        abort(404)
    code = generate_captcha_text(5)
    session[f"captcha_{form_type}"] = code
    session.modified = True
    img_io = create_captcha_image(code)
    response = make_response(send_file(img_io, mimetype="image/png"))
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")
        captcha = request.form.get("captcha", "").strip().upper()

        # Validate CAPTCHA
        expected_captcha = session.get("captcha_register", "").upper()
        if not expected_captcha or captcha != expected_captcha:
            session.pop("captcha_register", None)
            flash("Incorrect security code (CAPTCHA). Please try again.", "danger")
            return render_template("register.html", name=name, email=email, phone=phone)

        # Clear used captcha
        session.pop("captcha_register", None)

        if not name or not email or not password:
            flash("Please fill all required fields.", "danger")
            return render_template("register.html", name=name, email=email, phone=phone)

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template("register.html", name=name, email=email, phone=phone)

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "danger")
            return render_template("register.html", name=name, email=email, phone=phone)

        conn = get_db()
        cursor = conn.cursor()

        try:

            cursor.execute(
                """
                INSERT INTO users
                (name, email, phone, password, role, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    name,
                    email,
                    phone,
                    generate_password_hash(password),
                    "citizen",
                    datetime.now()
                )
            )

            conn.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(url_for("login"))

        except IntegrityError:

            flash(
                "An account with this email already exists.",
                "danger"
            )

        finally:

            cursor.close()
            conn.close()

    return render_template("register.html")


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        captcha = request.form.get("captcha", "").strip().upper()

        # Validate CAPTCHA
        expected_captcha = session.get("captcha_login", "").upper()
        if not expected_captcha or captcha != expected_captcha:
            session.pop("captcha_login", None)
            flash("Incorrect security code (CAPTCHA). Please try again.", "danger")
            return render_template("login.html", email=email)

        # Clear used captcha
        session.pop("captcha_login", None)

        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["name"] = user["name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))

            next_url = request.args.get("next") or request.form.get("next")
            if next_url and next_url.startswith("/") and not next_url.startswith("//"):
                return redirect(next_url)

            return redirect(url_for("dashboard"))

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template("login.html")


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("index"))


# ============================================================
# CITIZEN DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT *
        FROM issues
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (session["user_id"],)
    )

    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        issues=issues
    )


# ============================================================
# REPORT ISSUE
# ============================================================

@app.route("/report", methods=["GET", "POST"])
@login_required
def report_issue():

    if session.get("role") == "admin":
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()

        image = request.files.get("image")

        if not all([
            title,
            category,
            description,
            location
        ]):

            flash(
                "Please complete all required fields.",
                "danger"
            )

            return render_template(
                "report_issue.html",
                category=category
            )

        filename = None
        val_res = None
        img_phash = None

        if image and image.filename:

            if not allowed_file(image.filename):

                flash(
                    "Only PNG, JPG, JPEG and WEBP images are allowed.",
                    "danger"
                )

                return render_template(
                    "report_issue.html",
                    category=category
                )

            safe_name = secure_filename(
                image.filename
            )

            filename = (
                f"{datetime.now().strftime('%Y%m%d%H%M%S')}_"
                f"{session['user_id']}_"
                f"{safe_name}"
            )

            saved_path = os.path.join(
                UPLOAD_FOLDER,
                filename
            )
            image.save(saved_path)

            # Query existing image hashes for duplicate detection
            conn_h = get_db()
            cursor_h = conn_h.cursor()
            cursor_h.execute("SELECT image_phash FROM issues WHERE image_phash IS NOT NULL AND image_phash != ''")
            existing_hashes = [r[0] for r in cursor_h.fetchall()]
            cursor_h.close()
            conn_h.close()

            try:
                val_res = validate_civic_complaint(
                    saved_path,
                    description=description,
                    user_category=category,
                    existing_hashes=existing_hashes
                )
                img_phash = val_res.get("image_phash")
            except Exception:
                val_res = None

        now = datetime.now()

        # Decision & Validation values
        decision = val_res.get("decision", "ACCEPT") if val_res else "ACCEPT"
        val_status = decision
        pred_cat = val_res.get("predicted_category", category) if val_res else category
        ai_conf = float(val_res.get("ai_confidence", 85.0)) if val_res else 85.0
        ai_expl = val_res.get("explanation", "Complaint logged.") if val_res else "Complaint logged without photo."

        # Backend enforcement: If confirmed REJECT
        if val_res and decision == "REJECT":
            try:
                if saved_path and os.path.exists(saved_path):
                    os.remove(saved_path)
            except Exception:
                pass
            flash(
                f"Submission rejected by AI Validator: {ai_expl}. Please capture an authentic, clear photo of the municipal issue.",
                "danger"
            )
            return render_template(
                "report_issue.html",
                category=category,
                title=title,
                location=location,
                description=description
            )

        admin_note = f"[{decision} | Confidence: {ai_conf:.1f}% | Predicted: {pred_cat}] {ai_expl}"

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO issues
            (
                user_id,
                title,
                category,
                description,
                location,
                image,
                status,
                admin_note,
                validation_status,
                predicted_category,
                ai_confidence,
                review_decision,
                image_phash,
                ai_explanation,
                created_at,
                updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session["user_id"],
                title,
                category,
                description,
                location,
                filename,
                "Pending",
                admin_note,
                val_status,
                pred_cat,
                ai_conf,
                decision,
                img_phash,
                ai_expl,
                now,
                now
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        if val_res and decision == "MANUAL_REVIEW":
            flash(
                f"Your report has been submitted and queued for manual administrator review ({ai_expl}).",
                "warning"
            )
        else:
            flash(
                "Your civic issue has been verified and reported successfully.",
                "success"
            )

        return redirect(
            url_for("dashboard")
        )

    category = request.args.get("category", "").strip()

    return render_template(
        "report_issue.html",
        category=category
    )


# ============================================================
# AI IMAGE DETECTOR API
# ============================================================

@app.route("/api/ai-detect-image", methods=["POST"])
def api_ai_detect_image():
    if "image" not in request.files:
        return jsonify({"success": False, "error": "No image uploaded"}), 400

    file = request.files["image"]
    if not file or not file.filename:
        return jsonify({"success": False, "error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Unsupported file format. Please upload JPG, PNG or WEBP."}), 400

    try:
        temp_dir = os.path.join(UPLOAD_FOLDER, "_tmp")
        os.makedirs(temp_dir, exist_ok=True)
        safe_name = secure_filename(file.filename)
        temp_filename = f"scan_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{safe_name}"
        temp_path = os.path.join(temp_dir, temp_filename)
        file.save(temp_path)

        # Get existing image hashes for duplicate checking
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT image_phash FROM issues WHERE image_phash IS NOT NULL AND image_phash != ''")
        existing_hashes = [r[0] for r in cursor.fetchall()]
        cursor.close()
        conn.close()

        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()

        val = validate_civic_complaint(
            temp_path,
            description=description,
            user_category=category,
            existing_hashes=existing_hashes
        )

        try:
            os.remove(temp_path)
        except Exception:
            pass

        return jsonify({
            "success": True,
            "decision": val["decision"],
            "validation_status": val["validation_status"],
            "is_issue": val["decision"] == "ACCEPT",
            "confidence": val["ai_confidence"],
            "label": val["decision"],
            "category": val["predicted_category"],
            "reason": val["explanation"],
            "explanation": val["explanation"],
            "boxes": val.get("boxes", []),
            "is_blurry": val.get("is_blurry", False),
            "blur_score": val.get("blur_score", 0.0),
            "is_duplicate": val.get("is_duplicate", False),
            "is_ai_generated": val.get("is_ai_generated", False),
            "is_mismatch": val.get("is_mismatch", False),
            "text_analysis": val.get("text_analysis", {}),
            "image_analysis": val.get("image_analysis", {})
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500




# ============================================================
# ISSUE DETAILS
# ============================================================

@app.route("/issue/<int:issue_id>")
@login_required
def issue_detail(issue_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            issues.*,
            users.name,
            users.email,
            users.phone
        FROM issues
        JOIN users
            ON issues.user_id = users.id
        WHERE issues.id = %s
        """,
        (issue_id,)
    )

    issue = cursor.fetchone()

    cursor.close()
    conn.close()

    if not issue:

        flash(
            "Issue not found.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    if (
        session.get("role") != "admin"
        and issue["user_id"] != session["user_id"]
    ):

        flash(
            "You are not allowed to view this issue.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )

    ai_data = None
    if issue.get("image"):
        img_path = os.path.join(UPLOAD_FOLDER, issue["image"])
        if os.path.exists(img_path):
            try:
                ai_data = validate_civic_complaint(
                    img_path,
                    description=issue.get("description", ""),
                    user_category=issue.get("category", "")
                )
            except Exception:
                ai_data = None

    return render_template(
        "issue_detail.html",
        issue=issue,
        ai_data=ai_data
    )



# ============================================================
# UPLOADED FILE
# ============================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@app.route("/admin")
@admin_required
def admin_dashboard():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT COUNT(*) AS c FROM issues"
    )

    total = cursor.fetchone()["c"]

    cursor.execute(
        """
        SELECT COUNT(*) AS c
        FROM issues
        WHERE status = 'Pending'
        """
    )

    pending = cursor.fetchone()["c"]

    cursor.execute(
        """
        SELECT COUNT(*) AS c
        FROM issues
        WHERE status = 'In Progress'
        """
    )

    progress = cursor.fetchone()["c"]

    cursor.execute(
        """
        SELECT COUNT(*) AS c
        FROM issues
        WHERE status = 'Resolved'
        """
    )

    resolved = cursor.fetchone()["c"]

    cursor.execute(
        """
        SELECT COUNT(*) AS c
        FROM issues
        WHERE review_decision = 'MANUAL_REVIEW' OR validation_status = 'MANUAL_REVIEW'
        """
    )

    manual_review = cursor.fetchone()["c"]

    stats = {
        "total": total,
        "pending": pending,
        "progress": progress,
        "resolved": resolved,
        "manual_review": manual_review
    }

    cursor.execute(
        """
        SELECT
            issues.*,
            users.name AS citizen_name,
            users.email AS citizen_email
        FROM issues
        JOIN users
            ON issues.user_id = users.id
        ORDER BY issues.id DESC
        """
    )

    issues = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/dashboard.html",
        stats=stats,
        issues=issues
    )


# ============================================================
# ADMIN ISSUE
# ============================================================

@app.route(
    "/admin/issue/<int:issue_id>",
    methods=["GET", "POST"]
)
@admin_required
def admin_issue(issue_id):

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            issues.*,
            users.name AS citizen_name,
            users.email AS citizen_email,
            users.phone AS citizen_phone
        FROM issues
        JOIN users
            ON issues.user_id = users.id
        WHERE issues.id = %s
        """,
        (issue_id,)
    )

    issue = cursor.fetchone()

    if not issue:

        cursor.close()
        conn.close()

        flash(
            "Issue not found.",
            "danger"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    if request.method == "POST":

        status = request.form.get(
            "status",
            "Pending"
        )

        note = request.form.get(
            "admin_note",
            ""
        ).strip()

        if status not in {
            "Pending",
            "In Progress",
            "Resolved",
            "Rejected"
        }:

            status = "Pending"

        cursor.execute(
            """
            UPDATE issues
            SET
                status = %s,
                admin_note = %s,
                updated_at = %s
            WHERE id = %s
            """,
            (
                status,
                note,
                datetime.now(),
                issue_id
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

        flash(
            "Issue status updated.",
            "success"
        )

        return redirect(
            url_for(
                "admin_issue",
                issue_id=issue_id
            )
        )

    cursor.close()
    conn.close()

    ai_data = None
    if issue.get("image"):
        img_path = os.path.join(UPLOAD_FOLDER, issue["image"])
        if os.path.exists(img_path):
            try:
                ai_data = validate_civic_complaint(
                    img_path,
                    description=issue.get("description", ""),
                    user_category=issue.get("category", "")
                )
            except Exception:
                ai_data = None

    return render_template(
        "admin/issue.html",
        issue=issue,
        ai_data=ai_data
    )



# ============================================================
# ADMIN CITIZENS
# ============================================================

@app.route("/admin/citizens")
@admin_required
def admin_citizens():

    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            users.*,
            COUNT(issues.id) AS issue_count
        FROM users
        LEFT JOIN issues
            ON users.id = issues.user_id
        WHERE users.role = 'citizen'
        GROUP BY users.id
        ORDER BY users.id DESC
        """
    )

    citizens = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/citizens.html",
        citizens=citizens
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    init_db()

    app.run(debug=True, use_reloader=False)