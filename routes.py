from flask import Blueprint, request, jsonify, render_template, redirect, url_for
 from flask_login import login_user, logout_user, login_required, current_user
 from .models import User, Restaurant, Order, db  # Import your models
 from werkzeug.security import generate_password_hash, check_password_hash
 

 routes_bp = Blueprint('routes', __name__)
 

 # Authentication Routes
 @routes_bp.route('/auth/login', methods=['GET', 'POST'])
 def login():
  if request.method == 'POST':
  email = request.form.get('email')
  password = request.form.get('password')
  user = User.query.filter_by(email=email).first()
 

  if user and check_password_hash(user.password, password):
  login_user(user)
  return redirect(url_for('routes.dashboard'))  # Redirect to dashboard after login
  else:
  return render_template('login.html', error='Invalid credentials') # Ensure login.html exists
  return render_template('login.html')
 

 @routes_bp.route('/auth/register', methods=['GET', 'POST'])
 def register():
  if request.method == 'POST':
  email = request.form.get('email')
  name = request.form.get('name')
  password = request.form.get('password')
  role = request.form.get('role') # added
 

  hashed_password = generate_password_hash(password, method='sha256')
  new_user = User(email=email, name=name, password=hashed_password, role=role) # added role
 

  db.session.add(new_user)
  db.session.commit()
 

  return redirect(url_for('routes.login')) # Redirect to login after registration
  return render_template('register.html') # Ensure register.html exists
 

 @routes_bp.route('/auth/logout')
 @login_required
 def logout():
  logout_user()
  return redirect(url_for('routes.login')) #Redirect to login page after logout
 

 # Dashboard Route (Example - requires login)
 @routes_bp.route('/dashboard')
 @login_required
 def dashboard():
  # Example: Check user role and display different content
  if current_user.role == 'admin':
  return render_template('admin_dashboard.html')  # Admin dashboard
  elif current_user.role == 'restaurant':
  return render_template('restaurant_dashboard.html') # Restaurant dashboard
  elif current_user.role == 'driver':
  return render_template('driver_dashboard.html')  # Driver dashboard
  else: #Customer
  return render_template('customer_dashboard.html') #Customer dashboard
 

 # Restaurant Routes (Example)
 @routes_bp.route('/restaurants', methods=['GET'])
 @login_required
 def list_restaurants():
  restaurants = Restaurant.query.all()
  restaurant_list = [{'id': r.id, 'name': r.name, 'address': r.address} for r in restaurants]
  return jsonify(restaurants=restaurant_list)
 

 @routes_bp.route('/restaurants/<int:restaurant_id>', methods=['GET'])
 @login_required
 def get_restaurant(restaurant_id):
  restaurant = Restaurant.query.get_or_404(restaurant_id)
  return jsonify(id=restaurant.id, name=restaurant.name, address=restaurant.address)
 

 @routes_bp.route('/restaurants', methods=['POST'])
 @login_required
 def create_restaurant():
  if current_user.role != 'admin':
  return jsonify({'message': 'Unauthorized'}), 403
 

  data = request.get_json()
  new_restaurant = Restaurant(name=data['name'], address=data['address'])
  db.session.add(new_restaurant)
  db.session.commit()
  return jsonify({'message': 'Restaurant created successfully', 'id': new_restaurant.id}), 201
 

 # Order Routes (Example)
 @routes_bp.route('/orders', methods=['GET'])
 @login_required
 def list_orders():
  # Add role-based filtering here if needed (e.g., driver sees only assigned orders)
  orders = Order.query.all()
  order_list = [{'id': o.id, 'customer_id': o.customer_id, 'restaurant_id': o.restaurant_id, 'status': o.status} for o in orders]
  return jsonify(orders=order_list)
 

 @routes_bp.route('/orders/<int:order_id>', methods=['GET'])
 @login_required
 def get_order(order_id):
  order = Order.query.get_or_404(order_id)
  return jsonify(id=order.id, customer_id=order.customer_id, restaurant_id=order.restaurant_id, status=order.status)
 

 @routes_bp.route('/orders', methods=['POST'])
 @login_required
 def create_order():
  data = request.get_json()
  new_order = Order(customer_id=data['customer_id'], restaurant_id=data['restaurant_id'], status='pending')
  db.session.add(new_order)
  db.session.commit()
  return jsonify({'message': 'Order created successfully', 'id': new_order.id}), 201
 

 @routes_bp.route('/orders/<int:order_id>', methods=['PUT'])
 @login_required
 def update_order(order_id):
  order = Order.query.get_or_404(order_id)
  data = request.get_json()
  order.status = data['status']
  db.session.commit()
  return jsonify({'message': 'Order updated successfully'})
 

 # Example templates (ensure these exist in your 'templates' folder)
 # login.html, register.html, admin_dashboard.html, restaurant_dashboard.html, driver_dashboard.html, customer_dashboard.html