Civic Issues Reporting System
A final-year B.Tech CSE web project for reporting local civic problems.

Features
Citizen registration and login
Citizen dashboard
Report civic issue with category, description and location
Upload issue photo
Track issue status
View issue details
Admin login and dashboard
Admin can update status and add notes
Citizen management
MySQL database (civic_issues_db)
Responsive CSS
Technology
Python
Flask
MySQL (mysql-connector-python)
HTML5
CSS3
JavaScript
VS Code Setup
1. Install Python & MySQL
Install Python 3.10+ and MySQL Server (e.g. MySQL Community Server). Ensure MySQL service is running on localhost:3306.

2. Configure MySQL Database
Make sure the MySQL database civic_issues_db exists:

CREATE DATABASE IF NOT EXISTS civic_issues_db;
Verify DB_CONFIG credentials in app.py:

Host: localhost
Port: 3306
User: root
Password: <YOUR_MYSQL_PASSWORD>
Database: civic_issues_db
Test your connection anytime using:

python test_mysql.py
3. Open project
Open this folder in VS Code.

4. Create virtual environment
Windows:

python -m venv venv
venv\Scripts\activate
If PowerShell blocks activation:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
5. Install packages
pip install -r requirements.txt
6. Run
python app.py
7. Open browser
http://127.0.0.1:5000

The MySQL database civic_issues_db tables (users, issues) and default admin user are verified/initialized automatically on startup.

Demo Admin Login
Email: admin@civic.local Password: admin123

Change the admin password/secret before any real deployment.

Project Flow
Citizen -> Register -> Login -> Dashboard -> Report Issue -> Upload Photo -> Issue stored in MySQL (civic_issues_db) -> Admin Dashboard -> Update Status/Note -> Citizen checks status

Suggested future improvements
Email/SMS notifications
GPS/Google Maps integration
Department assignment
Search/filter
Priority/severity
Complaint comments
Analytics charts
Government department accounts
