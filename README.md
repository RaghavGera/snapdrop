Snapdrop

Snapdrop is a Flask + Socket.IO web app that allows users to sign up, log in, upload and download files, and exchange real-time messages between connected clients.
It includes authentication, file storage in SQLite, and a simple dashboard.

✨ Features

User Authentication

Sign up with email & password

Passwords hashed with Werkzeug for security

Login/logout flow with flash messages

File Management

Upload files (stored in /uploads and tracked in SQLite)

List uploaded files

Download by ID

Cleanup route to remove missing file records

Real-time Messaging

Socket.IO integrated for live message broadcasting between clients

Database

SQLite via SQLAlchemy ORM

Models: User, File

🛠️ Tech Stack

Backend: Flask, Flask-SocketIO, SQLAlchemy

Database: SQLite

Frontend: Jinja2 templates (index.html, login.html, upload.html)

Security: Werkzeug password hashing

📂 Project Structure
snapdrop/
├── app.py              # Main Flask app
├── templates/          # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   └── upload.html
├── static/             # CSS/JS files
├── uploads/            # Uploaded files (auto-created at runtime)
├── instance/           # DB & config (ignored in git recommended)
└── snapdrop.db         # SQLite database (created at runtime)

⚡ Installation & Setup
1. Clone the repo
git clone https://github.com/RaghavGera/snapdrop.git
cd snapdrop

2. Create & activate a virtual environment
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

3. Install dependencies

Create requirements.txt with:

flask
flask-socketio
flask-sqlalchemy
werkzeug


Then install:

pip install -r requirements.txt

4. Run the app
python app.py


Server runs at → http://127.0.0.1:5000

🚀 Usage

Home (/) → See uploaded files

Sign Up (/signup) → Create new user

Login (/login) → Authenticate user

Dashboard (/dashboard) → User dashboard (basic text for now)

Upload (/upload) → Upload a file

Uploads (/uploads) → View files

Download (/download/<id>) → Download file by ID

Cleanup (/cleanup) → Remove DB entries of missing files

WebSocket messages → Broadcasts between connected clients

🔒 Security Notes

Default SECRET_KEY is set as admin123 in app.py — replace it with an environment variable in production.

Do not commit real secrets or production DB.

Consider adding CSRF protection with Flask-WTF if you expand auth.

🛤️ Roadmap

 Add session-based login persistence

 Improve dashboard with file & message UI

 WebSocket-powered real-time file transfer (true “Snapdrop” behavior)

 Add Dockerfile & deployment guide

 CI pipeline with tests

