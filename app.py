from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import atexit

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'admin123'  # Set this to a secure random value
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///snapdrop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize extensions
db = SQLAlchemy(app)
socketio = SocketIO(app)

# Models
class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(200), nullable=False)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    files = File.query.all()
    return render_template('index.html', files=files)

@app.route('/loginsignup')
def loginsignup():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if valid_credentials(email, password):
        flash('Logged in successfully!', 'success')
        return redirect(url_for('dashboard'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('index'))

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('index'))
    if create_user(email, password):
        flash('Account created successfully! Please log in.', 'success')
    else:
        flash('Error creating account. Email may already be registered.', 'error')
    
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Add logic to check if the user is logged in
    return "Welcome to your dashboard!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_file = File(filename=filename, filepath=filepath)
            db.session.add(new_file)
            db.session.commit()
            return 'File uploaded successfully'
    return render_template('upload.html')

@app.route('/download/<int:file_id>')
def download_file(file_id):
    file = File.query.get(file_id)
    if file:
        return send_file(file.filepath, as_attachment=True)
    return 'File not found'

def valid_credentials(email, password):
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return True
    return False

def create_user(email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return False
    
    new_user = User(email=email)
    new_user.set_password(password)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        db.session.rollback()
        return False

# SocketIO event handler
@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

def cleanup():
    db_path = '/uploads/snapdrop.db'
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f'Deleted database file: {db_path}')

atexit.register(cleanup)

# Run the application
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)