/**
 * CivicReport Multi-Language Translation Engine (i18n)
 * Supported languages: English (en), Hindi / हिन्दी (hi), Marathi / मराठी (mr)
 */

const CIVIC_TRANSLATIONS = {
    en: {
        // Navigation & Branding
        "brand_name": "CivicReport",
        "brand_tagline": "Report • Track • Improve",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_features": "Features",
        "nav_contact": "Contact",
        "nav_login": "Login",
        "nav_register": "Register",
        "nav_logout": "Logout",
        "nav_dashboard": "Dashboard",
        "nav_my_dashboard": "My Dashboard",
        "nav_report_issue": "Report Issue",
        "nav_admin_dashboard": "Admin Dashboard",
        "nav_citizens": "Citizens",
        "nav_welcome": "Hi,",

        // Homepage Hero
        "hero_badge": "⚡ AI-Powered Civic Complaint System",
        "hero_heading": "Report Civic Issues Easy & Fast",
        "hero_desc": "Connect with local municipal authorities to fix potholes, streetlight outages, garbage accumulation, and water leaks in your neighborhood.",
        "hero_btn_report": "Report an Issue",
        "hero_btn_track": "Track Status",
        "hero_btn_works": "See How It Works",

        // Defect Cards
        "defect_garbage_title": "Garbage",
        "defect_garbage_sub": "Not Collected",
        "defect_streetlight_title": "Street Light",
        "defect_streetlight_sub": "Not Working",
        "defect_road_title": "Road",
        "defect_road_sub": "Damaged",
        "defect_water_title": "Water",
        "defect_water_sub": "Leakage",

        // How it works
        "hiw_eyebrow": "HOW IT WORKS",
        "hiw_heading": "Three Simple Steps to Fix Issues",
        "step1_title": "1. Capture & Upload",
        "step1_desc": "Take a clear photograph of the defect (pothole, garbage, leak).",
        "step2_title": "2. AI Validates & Routes",
        "step2_desc": "Our multi-modal AI verifies photo authenticity and notifies authorities.",
        "step3_title": "3. Fast Municipal Action",
        "step3_desc": "Field teams resolve the problem with status updates in real-time.",

        // Categories
        "cat_eyebrow": "ISSUE CATEGORIES",
        "cat_heading": "What Can You Report?",
        "cat_road": "Road & Potholes",
        "cat_road_desc": "Cracked roads, potholes, damaged asphalt and curbs.",
        "cat_light": "Streetlights",
        "cat_light_desc": "Flickering, broken, or unlit public street lamps.",
        "cat_waste": "Garbage & Waste",
        "cat_waste_desc": "Overflowing public bins, unattended rubbish piles.",
        "cat_water": "Water Supply",
        "cat_water_desc": "Burst pipes, drinking water leaks, contaminated lines.",
        "cat_drain": "Drainage & Sewage",
        "cat_drain_desc": "Blocked storm drains, open manholes, sewage overflow.",
        "cat_park": "Traffic & Parking",
        "cat_park_desc": "Illegal lane blockages, unauthorized parking, sign issues.",

        // CTA Banner & Footer
        "cta_heading": "Help Keep Our City Clean & Safe",
        "cta_desc": "Join thousands of active citizens making our community better every day.",
        "cta_btn": "Report an Issue Now",
        "footer_rights": "© 2026 CivicReport • Civic Issues Reporting System. All rights reserved.",

        // Authentication & CAPTCHA
        "login_title": "Welcome back",
        "login_subtitle": "Login to manage your civic reports.",
        "email_label": "Email address",
        "email_placeholder": "you@example.com",
        "password_label": "Password",
        "password_placeholder": "Enter password",
        "login_btn": "Login",
        "no_account": "Don't have an account?",
        "create_account_link": "Create account",

        "register_title": "Create citizen account",
        "register_subtitle": "Register to report and track local civic issues.",
        "name_label": "Full name *",
        "name_placeholder": "Your full name",
        "phone_label": "Phone number",
        "phone_placeholder": "10-digit mobile number",
        "confirm_password_label": "Confirm password *",
        "confirm_password_placeholder": "Re-enter password",
        "create_account_btn": "Create Account",
        "already_registered": "Already registered?",

        "captcha_label": "Security Verification (CAPTCHA) *",
        "captcha_placeholder": "Enter characters shown above",
        "captcha_refresh_title": "Click to change CAPTCHA",

        // Report Issue Form
        "report_page_title": "Report a Civic Issue",
        "report_page_subtitle": "Submit infrastructure problems directly to municipal authorities.",
        "issue_title_label": "Issue title *",
        "issue_title_placeholder": "Brief summary (e.g., Pothole on Main Road)",
        "category_label": "Category *",
        "category_select": "Select category",
        "location_label": "Location *",
        "location_placeholder": "Area, street, landmark, city",
        "desc_label": "Problem description *",
        "desc_placeholder": "Explain what happened, where it is, and how it affects people...",
        "photo_label": "Upload photo",
        "photo_choose": "📷 Choose an image (max 5 MB)",
        "submit_report_btn": "Submit Civic Report",
        "notice_pending": "Your report will initially be marked Pending. The admin can update its status after review.",

        // Dashboard
        "dashboard_eyebrow": "CITIZEN PORTAL",
        "dashboard_heading": "My Civic Reports",
        "dashboard_desc": "Track the issues you have reported.",
        "btn_report_new": "+ Report New Issue",
        "no_reports_title": "No reports yet",
        "no_reports_desc": "Have you noticed a civic problem? Report it here.",
        "report_first_btn": "Report First Issue"
    },

    hi: {
        // Navigation & Branding
        "brand_name": "CivicReport",
        "brand_tagline": "शिकायत • ट्रैक • सुधार",
        "nav_home": "होम",
        "nav_about": "के बारे में",
        "nav_features": "सुविधाएं",
        "nav_contact": "संपर्क",
        "nav_login": "लॉगिन",
        "nav_register": "पंजीकरण",
        "nav_logout": "लॉगआउट",
        "nav_dashboard": "डैशबोर्ड",
        "nav_my_dashboard": "मेरा डैशबोर्ड",
        "nav_report_issue": "समस्या दर्ज करें",
        "nav_admin_dashboard": "एडमिन डैशबोर्ड",
        "nav_citizens": "नागरिक सूची",
        "nav_welcome": "नमस्ते,",

        // Homepage Hero
        "hero_badge": "⚡ एआई आधारित नगर निगम शिकायत प्रणाली",
        "hero_heading": "नागरिक समस्याओं की शिकायत आसान और तेज़",
        "hero_desc": "अपने क्षेत्र में गड्ढे, बंद स्ट्रीट लाइट, कचरे के ढेर और पानी के रिसाव को ठीक करने के लिए स्थानीय नगर निगम से सीधे जुड़ें।",
        "hero_btn_report": "समस्या दर्ज करें",
        "hero_btn_track": "स्थिति ट्रैक करें",
        "hero_btn_works": "यह कैसे काम करता है",

        // Defect Cards
        "defect_garbage_title": "कचरा",
        "defect_garbage_sub": "उठाया नहीं गया",
        "defect_streetlight_title": "स्ट्रीट लाइट",
        "defect_streetlight_sub": "खराब है",
        "defect_road_title": "सड़क",
        "defect_road_sub": "क्षतिग्रस्त",
        "defect_water_title": "पानी",
        "defect_water_sub": "रिसाव",

        // How it works
        "hiw_eyebrow": "कार्यप्रणाली",
        "hiw_heading": "समस्या समाधान के तीन आसान कदम",
        "step1_title": "1. फोटो खींचें और अपलोड करें",
        "step1_desc": "समस्या (सड़क का गड्ढा, कचरा, लीकेज) का स्पष्ट फोटो लें।",
        "step2_title": "2. एआई सत्यापन और रूटिंग",
        "step2_desc": "हमारा एआई मॉडल फोटो की प्रामाणिकता जांचकर संबंधित विभाग को भेजता है।",
        "step3_title": "3. त्वरित नगरपालिका कार्रवाई",
        "step3_desc": "फील्ड टीमें समस्या का निवारण करती हैं और लाइव स्थिति अपडेट प्रदान करती हैं।",

        // Categories
        "cat_eyebrow": "समस्या श्रेणियां",
        "cat_heading": "आप किन समस्याओं की रिपोर्ट कर सकते हैं?",
        "cat_road": "सड़क और गड्ढे",
        "cat_road_desc": "टूटी सड़कें, गड्ढे, क्षतिग्रस्त डामर और फुटपाथ।",
        "cat_light": "स्ट्रीट लाइट",
        "cat_light_desc": "झिलमिलाती, टूटी हुई या बंद सार्वजनिक स्ट्रीट लाइटें।",
        "cat_waste": "कचरा और अपशिष्ट",
        "cat_waste_desc": "भरे हुए कूड़ेदान और लावारिस पड़े कचरे के ढेर।",
        "cat_water": "जल आपूर्ति",
        "cat_water_desc": "फटे हुए पाइप, पीने के पानी का रिसाव या दूषित पानी।",
        "cat_drain": "जल निकासी और सीवेज",
        "cat_drain_desc": "बंद नाले, खुले मैनहोल और सीवेज का रिसाव।",
        "cat_park": "यातायात और पार्किंग",
        "cat_park_desc": "अवैध रूप से रास्ते बंद करना, अनधिकृत पार्किंग।",

        // CTA Banner & Footer
        "cta_heading": "अपने शहर को स्वच्छ और सुरक्षित रखने में मदद करें",
        "cta_desc": "हजारों जागरूक नागरिकों के साथ जुड़ें और अपने समुदाय को रोज़ाना बेहतर बनाएं।",
        "cta_btn": "अभी समस्या दर्ज करें",
        "footer_rights": "© 2026 CivicReport • नागरिक समस्या निवारण प्रणाली। सर्वाधिकार सुरक्षित।",

        // Authentication & CAPTCHA
        "login_title": "फिर से स्वागत है",
        "login_subtitle": "अपनी नागरिक रिपोर्ट प्रबंधित करने के लिए लॉगिन करें।",
        "email_label": "ईमेल पता",
        "email_placeholder": "you@example.com",
        "password_label": "पासवर्ड",
        "password_placeholder": "पासवर्ड दर्ज करें",
        "login_btn": "लॉगिन करें",
        "no_account": "खाता नहीं है?",
        "create_account_link": "खाता बनाएं",

        "register_title": "नागरिक खाता बनाएं",
        "register_subtitle": "स्थानीय नागरिक समस्याओं की रिपोर्ट और ट्रैकिंग के लिए पंजीकरण करें।",
        "name_label": "पूरा नाम *",
        "name_placeholder": "आपका पूरा नाम",
        "phone_label": "फ़ोन नंबर",
        "phone_placeholder": "10 अंकों का मोबाइल नंबर",
        "confirm_password_label": "पासवर्ड की पुष्टि करें *",
        "confirm_password_placeholder": "पासवर्ड पुनः दर्ज करें",
        "create_account_btn": "खाता बनाएं",
        "already_registered": "पहले से पंजीकृत हैं?",

        "captcha_label": "सुरक्षा सत्यापन (कैप्चा) *",
        "captcha_placeholder": "ऊपर दिखाए गए अक्षर दर्ज करें",
        "captcha_refresh_title": "कैप्चा बदलने के लिए क्लिक करें",

        // Report Issue Form
        "report_page_title": "नागरिक समस्या की शिकायत दर्ज करें",
        "report_page_subtitle": "बुनियादी ढांचे की समस्याओं को सीधे नगरपालिका अधिकारियों को भेजें।",
        "issue_title_label": "समस्या का शीर्षक *",
        "issue_title_placeholder": "संक्षिप्त विवरण (उदा. मुख्य सड़क पर गड्ढा)",
        "category_label": "श्रेणी *",
        "category_select": "श्रेणी चुनें",
        "location_label": "स्थान *",
        "location_placeholder": "क्षेत्र, सड़क, लैंडमार्क, शहर",
        "desc_label": "समस्या का विवरण *",
        "desc_placeholder": "समझाएं कि क्या समस्या है, यह कहां है और इससे क्या परेशानी हो रही है...",
        "photo_label": "फोटो अपलोड करें",
        "photo_choose": "📷 फोटो चुनें (अधिकतम 5 MB)",
        "submit_report_btn": "नागरिक रिपोर्ट सबमिट करें",
        "notice_pending": "आपकी रिपोर्ट शुरू में 'लंबित' के रूप में चिह्नित की जाएगी। व्यवस्थापक समीक्षा के बाद इसे अपडेट करेंगे।",

        // Dashboard
        "dashboard_eyebrow": "नागरिक पोर्टल",
        "dashboard_heading": "मेरी नागरिक रिपोर्टें",
        "dashboard_desc": "आपके द्वारा रिपोर्ट की गई समस्याओं की स्थिति ट्रैक करें।",
        "btn_report_new": "+ नई समस्या दर्ज करें",
        "no_reports_title": "अभी तक कोई रिपोर्ट नहीं",
        "no_reports_desc": "क्या आपको कोई नागरिक समस्या दिखी है? यहाँ रिपोर्ट करें।",
        "report_first_btn": "पहली रिपोर्ट दर्ज करें"
    },

    mr: {
        // Navigation & Branding
        "brand_name": "CivicReport",
        "brand_tagline": "तक्रार • ट्रॅक • सुधारणा",
        "nav_home": "मुख्यपृष्ठ",
        "nav_about": "माहिती",
        "nav_features": "वैशिष्ट्ये",
        "nav_contact": "संपर्क",
        "nav_login": "लॉगिन",
        "nav_register": "नोंदणी",
        "nav_logout": "लॉगआउट",
        "nav_dashboard": "डॅशबोर्ड",
        "nav_my_dashboard": "माझे डॅशबोर्ड",
        "nav_report_issue": "तक्रार नोंदवा",
        "nav_admin_dashboard": "प्रशासक डॅशबोर्ड",
        "nav_citizens": "नागरिक सूची",
        "nav_welcome": "नमस्कार,",

        // Homepage Hero
        "hero_badge": "⚡ एआय आधारित महापालिका तक्रार प्रणाली",
        "hero_heading": "नागरी समस्यांची तक्रार सोपी आणि जलद",
        "hero_desc": "आपल्या परिसरातील खड्डे, बंद पथदिवे, कचऱ्याचे ढीग आणि पाण्याची गळती दुरुस्त करण्यासाठी स्थानिक महापालिकेशी थेट संपर्क साधा.",
        "hero_btn_report": "तक्रार नोंदवा",
        "hero_btn_track": "स्थिती तपासा",
        "hero_btn_works": "हे कसे कार्य करते",

        // Defect Cards
        "defect_garbage_title": "कचरा",
        "defect_garbage_sub": "गोळा केला नाही",
        "defect_streetlight_title": "पथदिवा",
        "defect_streetlight_sub": "बंद आहे",
        "defect_road_title": "रस्ता",
        "defect_road_sub": "खराब झाला आहे",
        "defect_water_title": "पाणी",
        "defect_water_sub": "गळती",

        // How it works
        "hiw_eyebrow": "कार्यपद्धती",
        "hiw_heading": "समस्या सोडवण्यासाठी तीन सोप्या पायऱ्या",
        "step1_title": "1. फोटो काढा आणि अपलोड करा",
        "step1_desc": "समस्येचा (रस्त्यावरील खड्डा, कचरा, गळती) स्पष्ट फोटो काढा.",
        "step2_title": "2. एआय पडताळणी आणि वर्गीकरण",
        "step2_desc": "आमची एआय प्रणाली फोटोची सत्यता तपासून संबंधित विभागाकडे पाठवते.",
        "step3_title": "3. त्वरित महापालिका कारवाई",
        "step3_desc": "फील्ड टीम समस्या सोडवते आणि रिअल-टाइम स्थिती अद्ययावत करते.",

        // Categories
        "cat_eyebrow": "समस्या प्रवर्ग",
        "cat_heading": "तुम्ही कोणती तक्रार नोंदवू शकता?",
        "cat_road": "रस्ते व खड्डे",
        "cat_road_desc": "खड्डे पडलेले रस्ते, तुटलेले डांबरीकरण आणि पदपथ.",
        "cat_light": "पथदिवे",
        "cat_light_desc": "बंद असलेले, लुकलुकणारे किंवा तुटलेले सार्वजनिक दिवे.",
        "cat_waste": "कचरा व सांडपाणी",
        "cat_waste_desc": "ओसंडून वाहणारे कचराकुंडी आणि अस्वच्छ कचऱ्याचे ढीग.",
        "cat_water": "पाणी पुरवठा",
        "cat_water_desc": "फुटलेल्या जलवाहिन्या, पिण्याच्या पाण्याची गळती किंवा दूषित पाणी.",
        "cat_drain": "ड्रेनेज व सांडपाणी",
        "cat_drain_desc": "तुंबलेली गटारे, उघडी मॅनहोल्स आणि सांडपाणी ओसंडणे.",
        "cat_park": "वाहतूक व पार्किंग",
        "cat_park_desc": "बेकायदेशीर रस्ता अडवणे, अनधिकृत पार्किंग समस्या.",

        // CTA Banner & Footer
        "cta_heading": "आपले शहर स्वच्छ आणि सुरक्षित ठेवण्यास मदत करा",
        "cta_desc": "हजारो सजग नागरिकांसोबत सामील व्हा आणि आपल्या शहराला दररोज अधिक चांगले बनवा.",
        "cta_btn": "आत्ताच तक्रार नोंदवा",
        "footer_rights": "© 2026 CivicReport • नागरी समस्या तक्रार निवारण प्रणाली. सर्व हक्क राखीव.",

        // Authentication & CAPTCHA
        "login_title": "पुन्हा स्वागत आहे",
        "login_subtitle": "आपल्या नागरी तक्रारी व्यवस्थापित करण्यासाठी लॉगिन करा.",
        "email_label": "ईमेल पत्ता",
        "email_placeholder": "you@example.com",
        "password_label": "पासवर्ड",
        "password_placeholder": "पासवर्ड प्रविष्ट करा",
        "login_btn": "लॉगिन करा",
        "no_account": "खाते नाही का?",
        "create_account_link": "खाते तयार करा",

        "register_title": "नागरिक खाते तयार करा",
        "register_subtitle": "स्थानिक नागरी समस्यांची तक्रार व मागोवा घेण्यासाठी नोंदणी करा.",
        "name_label": "पूर्ण नाव *",
        "name_placeholder": "आपले पूर्ण नाव",
        "phone_label": "फोन नंबर",
        "phone_placeholder": "10 अंकी मोबाईल क्रमांक",
        "confirm_password_label": "पासवर्ड पुष्टी करा *",
        "confirm_password_placeholder": "पासवर्ड पुन्हा प्रविष्ट करा",
        "create_account_btn": "खाते तयार करा",
        "already_registered": "आधीच नोंदणीकृत आहात?",

        "captcha_label": "सुरक्षा पडताळणी (कॅप्चा) *",
        "captcha_placeholder": "वर दाखवलेली अक्षरे प्रविष्ट करा",
        "captcha_refresh_title": "कॅप्चा बदलण्यासाठी क्लिक करा",

        // Report Issue Form
        "report_page_title": "नागरी समस्येची तक्रार नोंदवा",
        "report_page_subtitle": "पायाभूत सुविधांच्या समस्या थेट महापालिका अधिकाऱ्यांकडे पाठवा.",
        "issue_title_label": "समस्येचे शीर्षक *",
        "issue_title_placeholder": "थोडक्यात सारांश (उदा. मुख्य रस्त्यावर खड्डा)",
        "category_label": "प्रवर्ग *",
        "category_select": "प्रवर्ग निवडा",
        "location_label": "ठिकाण *",
        "location_placeholder": "परिसर, रस्ता, लँडमार्क, शहर",
        "desc_label": "समस्येचे सविस्तर वर्णन *",
        "desc_placeholder": "समस्या काय आहे, कुठे आहे आणि नागरिकांना काय त्रास होतो ते सांगा...",
        "photo_label": "फोटो अपलोड करा",
        "photo_choose": "📷 फोटो निवडा (कमाल 5 MB)",
        "submit_report_btn": "तक्रार सबमिट करा",
        "notice_pending": "आपली तक्रार सुरुवातीला 'प्रलंबित' म्हणून नोंदवली जाईल. प्रशासक पुनरावलोकनानंतर तिची स्थिती अद्ययावत करतील.",

        // Dashboard
        "dashboard_eyebrow": "नागरिक पोर्टल",
        "dashboard_heading": "माझ्या नागरी तक्रारी",
        "dashboard_desc": "तुम्ही नोंदवलेल्या समस्यांचा मागोवा घ्या.",
        "btn_report_new": "+ नवीन तक्रार नोंदवा",
        "no_reports_title": "अद्याप कोणतीही तक्रार नाही",
        "no_reports_desc": "आपल्याला काही नागरी समस्या आढळली आहे का? येथे तक्रार करा.",
        "report_first_btn": "पहिली तक्रार नोंदवा"
    }
};

const LANG_CONFIG = {
    en: { name: "English", flag: "🇬🇧" },
    hi: { name: "हिन्दी", flag: "🇮🇳" },
    mr: { name: "मराठी", flag: "🇮🇳" }
};

/**
 * Apply translations to DOM elements based on data attributes
 */
function applyTranslations(lang) {
    if (!CIVIC_TRANSLATIONS[lang]) lang = "en";
    const dict = CIVIC_TRANSLATIONS[lang];

    // Translate textContent
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Translate innerHTML if formatted
    document.querySelectorAll("[data-i18n-html]").forEach(el => {
        const key = el.getAttribute("data-i18n-html");
        if (dict[key]) {
            el.innerHTML = dict[key];
        }
    });

    // Translate input placeholders
    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        if (dict[key]) {
            el.setAttribute("placeholder", dict[key]);
        }
    });

    // Translate titles / tooltips
    document.querySelectorAll("[data-i18n-title]").forEach(el => {
        const key = el.getAttribute("data-i18n-title");
        if (dict[key]) {
            el.setAttribute("title", dict[key]);
        }
    });

    // Update Language Button labels in the DOM
    document.querySelectorAll(".currentLangText").forEach(el => {
        el.textContent = LANG_CONFIG[lang].name;
    });
    document.querySelectorAll(".currentLangFlag").forEach(el => {
        el.textContent = LANG_CONFIG[lang].flag;
    });

    // Update active highlight on dropdown items
    document.querySelectorAll(".lang-option").forEach(btn => {
        if (btn.getAttribute("data-lang") === lang) {
            btn.classList.add("active");
        } else {
            btn.classList.remove("active");
        }
    });

    document.documentElement.lang = lang;
}

/**
 * Change language and persist preference
 */
window.setCivicLanguage = function(lang) {
    if (!CIVIC_TRANSLATIONS[lang]) lang = "en";
    try {
        localStorage.setItem("civic_lang", lang);
        document.cookie = "civic_lang=" + lang + ";path=/;max-age=31536000;SameSite=Lax";
    } catch (e) {
        console.warn("Storage not available for language preference");
    }
    applyTranslations(lang);
};

// Initialize language switcher on DOM load
document.addEventListener("DOMContentLoaded", function () {
    let savedLang = "en";
    try {
        savedLang = localStorage.getItem("civic_lang") || "en";
    } catch (e) {
        savedLang = "en";
    }
    if (!CIVIC_TRANSLATIONS[savedLang]) savedLang = "en";

    // Setup Dropdown Toggle Buttons
    document.querySelectorAll(".lang-btn").forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.stopPropagation();
            const parent = this.closest(".lang-switch-dropdown");
            if (parent) {
                parent.classList.toggle("open");
                const isOpen = parent.classList.contains("open");
                this.setAttribute("aria-expanded", isOpen ? "true" : "false");
            }
        });
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", function (e) {
        if (!e.target.closest(".lang-switch-dropdown")) {
            document.querySelectorAll(".lang-switch-dropdown.open").forEach(dropdown => {
                dropdown.classList.remove("open");
                const btn = dropdown.querySelector(".lang-btn");
                if (btn) btn.setAttribute("aria-expanded", "false");
            });
        }
    });

    // Handle Option Selection
    document.querySelectorAll(".lang-option").forEach(opt => {
        opt.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
            const chosenLang = this.getAttribute("data-lang");
            window.setCivicLanguage(chosenLang);

            // Close dropdown
            const parent = this.closest(".lang-switch-dropdown");
            if (parent) {
                parent.classList.remove("open");
                const btn = parent.querySelector(".lang-btn");
                if (btn) btn.setAttribute("aria-expanded", "false");
            }
        });
    });

    // Apply translations on load
    applyTranslations(savedLang);
});

