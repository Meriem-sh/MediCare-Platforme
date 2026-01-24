═══════════════════════════════════════════════════════════════════════════════
                                
                           👥  G R O U P   M E M B E R S
                                
═══════════════════════════════════════════════════════════════════════════════

    • Mehni Meriem
    • Sahali Meriem  
    • Riabi Yousra


═══════════════════════════════════════════════════════════════════════════════
                                
                  🏥  M E D I C A R E   P L A T F O R M
                 Doctor–Patient Medication Management Platform
                                
═══════════════════════════════════════════════════════════════════════════════

Medicare is a Django-based web application for medication management.
It allows secure management of drugs, prescriptions, reminders, and users 
through a containerized architecture using Docker.

The platform provides role-based access with dedicated dashboards for 
administrators, doctors, and patients.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                            ✨  F E A T U R E S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏠  HOME PAGE
    ├─ Platform information
    ├─ Login as admin
    ├─ Login as user (doctor / patient)
    └─ Create an account

👨‍💼  ADMIN DASHBOARD
    ├─ Full platform management
    ├─ Enhanced UI with custom branding
    └─ Optimized logout functionality

👨‍⚕️  DOCTOR DASHBOARD
    ├─ Create prescriptions
    ├─ Send medication reminders to patients
    ├─ Checks the adherence of taken drugs
    ├─ View patient profiles
    └─ Track rare disease patients

🧑‍⚕️  PATIENT DASHBOARD
    ├─ View prescriptions
    ├─ Receive reminders
    ├─ Track medication adherence
    ├─ Find specialist doctors
    └─ Assign personal doctor

👤  USER FEATURES
    ├─ Profile management
    ├─ Settings page
    ├─ Password change functionality
    └─ Welcome email notification on signup


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        📦  D J A N G O   A P P S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤  users          Authentication and user management
                   • Patients (regular / rare diseases)
                   • Doctors (generalists / specialists)
                   • Custom user model with extended fields
                   • Profile and settings management

💊  drugs          Drug catalog and drug-related data
                   • Disease classification
                   • Rare disease tracking

📋  prescriptions  Creation and tracking of prescriptions
                   • Doctor-patient prescription management
                   • Dosage and frequency tracking

⏰  reminders      Medication reminders and scheduling
                   • Dose logging system
                   • Adherence tracking


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        🛠️  T E C H   S T A C K

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️   Django (Python)                  🐘  PostgreSQL (Dockerized database)
📮  Redis / Upstash Redis            🐳  Docker & Docker Compose
🌐  NGINX (reverse proxy)            🔒  SSL / HTTPS
🦄  Gunicorn (WSGI server)           🎨  WhiteNoise (Static files)
☁️   Render.com (Cloud deployment)   📊  UptimeRobot (Monitoring)
📧  SMTP Email (Gmail)               🎯  Bootstrap 5 & Font Awesome


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                      🎲  G E N E R A T E D   D A T A

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥  Users           Custom users (Admins: 2, Doctors: 5, Patients: 10)
💊  Drugs           Drugs (10)
🦠  Diseases        Diseases (6)
📋  Prescriptions   Prescriptions (15)
⏰  Reminders       Reminders (20)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  📁  S T A T I C   F I L E S   M A N A G E M E N T

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂  static/
    Contains source static files used during development by Django apps.
    ├─ css/              Stylesheets (unified design system)
    ├─ js/               JavaScript files
    └─ images/           Logo and images (including logo-Medicare.jpg)

📂  staticfiles/
    Contains collected static files generated by `collectstatic`.
    This directory is served directly by NGINX in production for better 
    performance.

🎨  WhiteNoise
    Used in production (Render) for efficient static file serving without NGINX.
    156 static files collected automatically during deployment.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        🚀  D E P L O Y M E N T

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│              💻  L O C A L   D E V E L O P M E N T                          │
│                      ( Docker Desktop )                                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

The project is deployed locally using Docker Desktop with the following 
services:

  🐳  Django web service (`chapter17-web`)
  🐘  PostgreSQL database
  📮  Redis cache
  🌐  NGINX reverse proxy

NGINX is responsible for:
  ├─ Serving static files from `staticfiles/`
  ├─ Acting as a reverse proxy for Django
  └─ Handling SSL certificates to enable HTTPS


┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│          ☁️   P R O D U C T I O N   D E P L O Y M E N T                     │
│                        ( Render.com )                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

The project is deployed on Render.com with the following configuration:

  🦄  Web Service: Gunicorn WSGI server
  🐘  Database: PostgreSQL (managed by Render)
  📮  Cache: Upstash Redis (serverless Redis for session and caching)
  🎨  Static Files: WhiteNoise middleware
  🔒  SSL/HTTPS: Automatically enabled by Render
  🔄  Auto-deploy: Enabled from GitHub repository (main branch)
  📊  Monitoring: UptimeRobot (keeps service awake)
  📧  Email: SMTP configured with Gmail

Upstash Redis Role:
  • Session management
  • Django caching backend
  • Real-time data caching
  • WebSocket channel layer (for Django Channels)


┌─────────────────────────────────────────────────────────────────────────────┐
│          📋  D E P L O Y M E N T   P R O C E S S                            │
└─────────────────────────────────────────────────────────────────────────────┘

  1️⃣   Code pushed to GitHub
  2️⃣   Render automatically detects changes
  3️⃣   Builds Docker image
  4️⃣   Runs migrations
  5️⃣   Collects static files
  6️⃣   Creates admin users
  7️⃣   Generates fake data (if enabled)
  8️⃣   Starts Gunicorn server


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  🌐  D O M A I N   &   S E C U R I T Y

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🏠  Local Domain (Docker)
    └─ https://medicareproject/

☁️   Production Domain (Render)
    └─ https://medicare-platform-bjlp.onrender.com

🔒  HTTPS enabled using SSL certificates
📝  Sensitive configuration stored in `.env` file

⚠️   The `.env` file is excluded from version control.


┌─────────────────────────────────────────────────────────────────────────────┐
│                   👨‍💼  A D M I N   A C C E S S                               │
└─────────────────────────────────────────────────────────────────────────────┘

🔗  Admin Panel: https://medicare-platform-bjlp.onrender.com/admin/

👤  Admin Credentials:
    • Username: admin-Meriem-Sh
    • Password: Meriem-2003-12-25

👤  Second Admin:
    • Username: Meriem-Mh
    • Password: Meriem-2004-02-14


┌─────────────────────────────────────────────────────────────────────────────┐
│                     🧪  T E S T   U S E R S                                 │
└─────────────────────────────────────────────────────────────────────────────┘

👨‍⚕️  Doctor Login (5 accounts):
    • Usernames: doctor1, doctor2, doctor3, doctor4, doctor5
    • Password (same for all): doctor123

🧑‍⚕️  Patient Login (10 accounts):
    • Usernames: patient1, patient2, patient3, ..., patient10
    • Password (same for all): patient123


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              🔗  I M P O R T A N T   A D M I N   U R L S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👥  Users Management     /admin/users/customuser/
🦠  Diseases            /admin/drugs/disease/
💊  Drugs               /admin/drugs/drug/
📋  Prescriptions       /admin/prescriptions/prescription/
⏰  Reminders           /admin/reminders/reminder/
📊  Dose Logs           /admin/reminders/doselog/
🔐  Groups & Permissions /admin/auth/


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  ⚙️   R U N   W I T H   D O C K E R

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀  Build and start the containers:

    docker compose up --build

🛑  Stop the containers:

    docker compose down


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  ☁️   D E P L O Y   T O   R E N D E R

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣   Push code to GitHub repository
2️⃣   Connect repository to Render
3️⃣   Configure environment variables in Render Dashboard
4️⃣   Deploy automatically on every push to main branch


┌─────────────────────────────────────────────────────────────────────────────┐
│      📋  R E Q U I R E D   E N V I R O N M E N T   V A R I A B L E S        │
└─────────────────────────────────────────────────────────────────────────────┘

• DATABASE_URL (auto-generated by Render PostgreSQL service)
• REDIS_URL (from Upstash.com console after creating Redis database)
• DJANGO_SETTINGS_MODULE=medicare.settings.prod
• DEBUG=False
• ALLOWED_HOSTS=medicare-platform-bjlp.onrender.com
• LOAD_FAKE_DATA=True (optional)
• Admin credentials (ADMIN1_USERNAME, ADMIN1_PASSWORD, etc.)
• EMAIL_HOST_USER (Gmail address for sending emails)
• EMAIL_HOST_PASSWORD (Gmail App Password)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

              💤  K E E P   S E R V I C E   A W A K E

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Render free tier services sleep after 15 minutes of inactivity.
To keep your service always awake and responsive:

🔄  Setup UptimeRobot (Free Monitoring Service):

1. Create account at: https://uptimerobot.com
2. Click "Add New Monitor"
3. Configure monitor:
   • Monitor Type: HTTP(s)
   • Friendly Name: Medicare Platform
   • URL: https://medicare-platform-bjlp.onrender.com
   • Monitoring Interval: Every 5 minutes
4. Click "Create Monitor"

✅ Result: Your service will stay awake 24/7 with no cold start delays.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  📧  E M A I L   C O N F I G U R A T I O N

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅  SMTP Email Configured (Gmail)

📤  Email Features:
    • Welcome email sent on user signup
    • Password reset emails
    • Notification system ready for future enhancements

🔧  Configuration:
    • Backend: django.core.mail.backends.smtp.EmailBackend
    • Host: smtp.gmail.com
    • Port: 587 (TLS)
    • Configured via environment variables in Render


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

          🎨  U I / U X   I M P R O V E M E N T S   &   F I X E S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅  Template Enhancements:
    • Fixed Profile & Settings navigation links
    • Added "Back to Dashboard" buttons on all pages
    • Optimized Quick Actions button sizes
    • Unified logo display across all pages
    • Improved form styling and error handling

✅  Performance Optimizations:
    • Database query optimization with select_related()
    • Fixed N+1 query problems
    • Reduced page load times

✅  Admin Panel Improvements:
    • Custom branding with logo
    • Enhanced header and footer styling
    • Fixed logout functionality
    • Improved color scheme and UI consistency

✅  Responsive Design:
    • Mobile-friendly navigation
    • Bootstrap 5 integration
    • Consistent spacing and alignment


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                🔮  U P C O M I N G   F E A T U R E S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄  Planned Enhancements:

    ⏳  Email Verification System
        • User email confirmation on signup
        • Secure token-based verification
        • Account activation workflow

    ⏳  Automated Reminder Emails
        • Scheduled daily medication reminders
        • Celery + Redis task queue integration
        • Personalized email notifications

    ⏳  Advanced Analytics
        • Enhanced adherence tracking
        • Patient health reports
        • Doctor performance metrics


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  ✅  P R O J E C T   S T A T U S

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                  🎉  F U L L Y   D E P L O Y E D   A N D   F U N C T I O N A L

✅  Django application running on Render
✅  PostgreSQL database connected
✅  Upstash Redis cache operational
✅  Static files served via WhiteNoise
✅  SSL/HTTPS enabled
✅  Admin panel accessible
✅  Fake data generated successfully
✅  All models and relationships working correctly
✅  UptimeRobot monitoring active
✅  Email notifications configured
✅  UI/UX optimizations completed
✅  Performance improvements implemented
✅  Mobile responsive design

📅  Initial Deployment: January 9, 2026
🔄  Latest Update: January 23, 2026
🚀  Status: Live and running 🎉


═══════════════════════════════════════════════════════════════════════════════
                                
                      🎯  E N D   O F   D O C U M E N T A T I O N
                                
═══════════════════════════════════════════════════════════════════════════════
