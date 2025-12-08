import os

print("🔧 FIXING SUPREME DELIVERY APP...")

# --- CORRECTED APP.PY ---
app_code = """import os
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO

# Setup Flask
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'delivery.db')
app.config['SECRET_KEY'] = 'grabfood-secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# --- MODELS ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer') # customer, restaurant, driver

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='Pending')
    total = db.Column(db.Float, default=0.0)

# --- WEB PORTALS (The GrabFood Experience) ---
@app.route('/')
def landing():
    # Main Entry Point - Login Page
    return render_template('login.html')

@app.route('/customer/home')
def customer_home():
    return render_template('customer/home.html')

@app.route('/restaurant/dashboard')
def restaurant_dashboard():
    return render_template('restaurant/dashboard.html')

# --- API ROUTES (LOGIN LOGIC) ---
@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Universal Login for Demo
    role = "customer"
    redirect_url = "/customer/home"
    
    if username == "admin": 
        role = "restaurant"
        redirect_url = "/restaurant/dashboard"
    elif username == "driver":
        role = "driver"
        redirect_url = "/driver/home"

    return jsonify({
        "status": "success", 
        "token": "supreme-token", 
        "role": role,
        "redirect": redirect_url
    }), 200

# --- SOCKETS (Real-Time Tracking) ---
@socketio.on('connect')
def handle_connect():
    print('⚡ Client Connected')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Create Default Users
        if not User.query.filter_by(username='admin').first():
            print("⚡ Creating Mock Users (admin, user, driver)...")
            db.session.add(User(username='admin', password='123', role='restaurant'))
            db.session.add(User(username='user', password='123', role='customer'))
            db.session.add(User(username='driver', password='123', role='driver'))
            db.session.commit()
            
    print("🍔 SUPREME DELIVERY ONLINE: http://127.0.0.1:5000")
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("✅ app.py FIXED. Imports and Routes corrected.")