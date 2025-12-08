from flask import Flask
 from flask_sqlalchemy import SQLAlchemy
 from flask_socketio import SocketIO
 from flask_login import LoginManager
 from os import path

 db = SQLAlchemy()
 socketio = SocketIO()
 DB_NAME = "database.db"

 def create_app():
  app = Flask(__name__)
  app.config['SECRET_KEY'] = 'supersecretkey123'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from .models import User

  @login_manager.user_loader
  def load_user(id):
   return User.query.get(int(id))

  from .auth import auth as auth_blueprint
  from .customer import customer as customer_blueprint
  from .restaurant import restaurant as restaurant_blueprint
  from .driver import driver as driver_blueprint

  app.register_blueprint(auth_blueprint, url_prefix='/auth')
  app.register_blueprint(customer_blueprint, url_prefix='/customer')
  app.register_blueprint(restaurant_blueprint, url_prefix='/restaurant')
  app.register_blueprint(driver_blueprint, url_prefix='/driver')

  from . import models

  with app.app_context():
   create_database(app)

  socketio.init_app(app)

  return app

 def create_database(app):
  if not path.exists('instance/' + DB_NAME):
   db.create_all()
   print('Created Database!')

 if __name__ == '__main__':
  app = create_app()
  socketio.run(app, debug=True)