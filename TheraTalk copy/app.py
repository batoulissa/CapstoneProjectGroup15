from flask import Flask
from db import db
from models import Therapist, Patient  # Import models without db
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/')
def home():
    return jsonify({'message': 'Hello from the backend!'})

if __name__ == '__main__':
    app.run(debug=True)


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'mysecretkey')

db.init_app(app)

# Create tables if they don't exist already
with app.app_context():
    db.create_all()

from models import db, Therapist, Patient  # Import db and models
from routes.auth_routes import auth_routes
from routes.patient_routes import patient_routes
from routes.therapist_routes import therapist_routes
from routes.matching_routes import matching_routes
from routes.admin_routes import admin_routes

# Register blueprints
app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(patient_routes, url_prefix='/patient')
app.register_blueprint(therapist_routes, url_prefix='/therapist')
app.register_blueprint(matching_routes, url_prefix='/match')
app.register_blueprint(admin_routes, url_prefix='/admin')

# Define a simple route to test if the app is running
@app.route('/')
def home():
    return "TheraTalk API is running!"

if __name__ == '__main__':
    app.run(debug=True)
