from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

db = SQLAlchemy()

class UserRole(enum.Enum):
    ADMIN = 'admin'
    RESTAURANT = 'restaurant'
    DRIVER = 'driver'
    CUSTOMER = 'customer'

class OrderStatus(enum.Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)
    restaurant = db.relationship('Restaurant', backref='owner', uselist=False)
    driver_location = db.relationship('DriverLocation', backref='driver', uselist=False)
    orders = db.relationship('Order', backref='customer')

    def __repr__(self):
        return f'<User {self.username}>'

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    menu_items = db.relationship('MenuItem', backref='restaurant')
    orders = db.relationship('Order', backref='restaurant')

    def __repr__(self):
        return f'<Restaurant {self.name}>'

class MenuItem(db.Model):
    __tablename__ = 'menu_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    total_amount = db.Column(db.Float, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    driver = db.relationship('User', foreign_keys=[driver_id])

    def __repr__(self):
        return f'<Order {self.id}>'

class DriverLocation(db.Model):
    __tablename__ = 'driver_locations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DriverLocation {self.user_id}>'