
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# The database file is in the instance folder in the project root.
db_path = os.path.join(os.getcwd(), 'instance', 'musicfly.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    try:
        users = User.query.all()
        if users:
            print("Here are the users in the database:")
            for user in users:
                print(f"  - ID: {user.id}, Username: {user.username}")
        else:
            print("There are no users in the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
