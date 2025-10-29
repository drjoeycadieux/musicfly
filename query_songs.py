
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# The database file is in the instance folder in the project root.
db_path = os.path.join(os.getcwd(), 'instance', 'musicfly.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Song(db.Model):
    __tablename__ = 'song'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255))
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

with app.app_context():
    try:
        songs = Song.query.all()
        if songs:
            print("Here are the songs in the database:")
            for song in songs:
                print(f"  - ID: {song.id}, Filename: {song.filename}, Title: {song.title}, Upload Time: {song.upload_time}")
        else:
            print("There are no songs in the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
