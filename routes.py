from flask import Flask, request, jsonify
 from flask_sqlalchemy import SQLAlchemy
 from functools import wraps
 import jwt
 import datetime
 

 app = Flask(__name__)
 app.config['SECRET_KEY'] = 'your_secret_key'
 app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory for simplicity
 app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 db = SQLAlchemy(app)
 

 # Database Models
 class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)
  role = db.Column(db.String(20), default='customer')  # 'customer', 'restaurant', 'admin'
 

 class Restaurant(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  address = db.Column(db.String(200))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Restaurant owner
  user = db.relationship('User', backref=db.backref('restaurants', lazy=True))
 

 class Order(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)
  order_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  status = db.Column(db.String(20), default='pending') # pending, accepted, rejected, delivered
 

 # Create the database tables
 with app.app_context():
  db.create_all()
 

 # Authentication Decorator
 def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
  token = request.headers.get('Authorization')
  if not token:
  return jsonify({'message': 'Token is missing!'}), 401
 

  try:
  token = token.split(" ")[1]
  data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
  current_user = User.query.filter_by(id=data['user_id']).first()
  except:
  return jsonify({'message': 'Token is invalid!'}), 401
 

  return f(current_user, *args, **kwargs)
  return decorated
 

 # Role-Based Access Decorator
 def role_required(role):
  def decorator(f):
  @wraps(f)
  def decorated_function(current_user, *args, **kwargs):
  if current_user.role != role:
  return jsonify({'message': 'Insufficient privileges!'}), 403
  return f(current_user, *args, **kwargs)
  return decorated_function
  return decorator
 

 # Authentication Routes
 @app.route('/auth/register', methods=['POST'])
 def register():
  data = request.get_json()
 

  hashed_password = data['password'] # In real app, hash this with bcrypt
 

  new_user = User(username=data['username'], password=hashed_password, role=data.get('role', 'customer')) # Default to customer role
 

  db.session.add(new_user)
  db.session.commit()
 

  return jsonify({'message': 'Registered successfully'}), 201
 

 @app.route('/auth/login', methods=['POST'])
 def login():
  auth = request.authorization
 

  if not auth or not auth.username or not auth.password:
  return jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
 

  user = User.query.filter_by(username=auth.username).first()
 

  if not user or user.password != auth.password: # In real app, compare hashed passwords
  return jsonify({'message': 'Could not verify'}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}
 

  token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'], algorithm="HS256")
 

  return jsonify({'token': token})
 

 # Order Routes (Example)
 @app.route('/orders', methods=['POST'])
 @token_required
 def create_order(current_user):
  data = request.get_json()
  restaurant_id = data.get('restaurant_id')
 

  if not restaurant_id:
  return jsonify({'message': 'Restaurant ID is required'}), 400
 

  restaurant = Restaurant.query.get(restaurant_id)
  if not restaurant:
  return jsonify({'message': 'Restaurant not found'}), 400
 

  new_order = Order(customer_id=current_user.id, restaurant_id=restaurant_id)
  db.session.add(new_order)
  db.session.commit()
 

  return jsonify({'message': 'Order created successfully'}), 201
 

 @app.route('/orders', methods=['GET'])
 @token_required
 def get_orders(current_user):
  orders = Order.query.filter_by(customer_id=current_user.id).all()
  output = []
  for order in orders:
  order_data = {}
  order_data['id'] = order.id
  order_data['restaurant_id'] = order.restaurant_id
  order_data['order_date'] = str(order.order_date)
  order_data['status'] = order.status
  output.append(order_data)
 

  return jsonify({'orders': output})
 

 

 # Restaurant Routes
 @app.route('/restaurants', methods=['POST'])
 @token_required
 @role_required('restaurant')
 def create_restaurant(current_user):
  data = request.get_json()
 

  new_restaurant = Restaurant(name=data['name'], address=data['address'], user_id=current_user.id)
  db.session.add(new_restaurant)
  db.session.commit()
 

  return jsonify({'message': 'Restaurant created successfully'}), 201
 

 @app.route('/restaurants', methods=['GET'])
 def get_restaurants():
  restaurants = Restaurant.query.all()
  output = []
  for restaurant in restaurants:
  restaurant_data = {}
  restaurant_data['id'] = restaurant.id
  restaurant_data['name'] = restaurant.name
  restaurant_data['address'] = restaurant.address
  output.append(restaurant_data)
 

  return jsonify({'restaurants': output})
 

 if __name__ == '__main__':
  app.run(debug=True)