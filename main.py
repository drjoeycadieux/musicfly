import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime

# ------------------- Config -------------------
app = Flask(__name__)

# File upload config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Allow uploads up to 1 GB (1 * 1024 * 1024 * 1024 bytes)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024
  # 50 MB max upload

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg'}

# Database config
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///music.db")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------- Models -------------------
class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

# ------------------- Initialize Database -------------------
with app.app_context():
    db.create_all()  # Create tables safely inside app context

# ------------------- Helpers -------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------- Routes -------------------
@app.route("/")
def index():
    songs = Song.query.order_by(Song.upload_time.desc()).all()
    return render_template("index.html", songs=songs)

@app.route("/upload", methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        song = Song(filename=filename)
        db.session.add(song)
        db.session.commit()

        return redirect(url_for('index'))
    else:
        return "File type not allowed", 400

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ------------------- Run -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
