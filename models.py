from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
import datetime

db = SQLAlchemy()

class Role(Enum):
    USER = 'user'
    RESTAURANT = 'restaurant'
    DRIVER = 'driver'
    ADMIN = 'admin'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Enum(Role), default=Role.USER)
    restaurant = db.relationship('Restaurant', backref='owner', uselist=False)
    orders = db.relationship('Order', backref='customer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    menu_items = db.relationship('Menu', backref='restaurant')

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f'<Menu Item {self.name}>'

class OrderStatus(Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    PREPARING = 'preparing'
    EN_ROUTE = 'en_route'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
    items = db.Column(db.String(500), nullable=False) # Store item IDs as comma-separated string
    total_amount = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Assuming drivers are also users
    restaurant = db.relationship('Restaurant')

    def __repr__(self):
        return f'<Order {self.id}>'

class DriverLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    driver = db.relationship('User')

    def __repr__(self):
        return f'<DriverLocation {self.driver_id}>'