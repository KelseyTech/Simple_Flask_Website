from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
#This allows us to change our database name
DB_NAME = "database.db"

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'DAWODAWODMAWD'
    #This is the path to our database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #This means our database starts with our application

    
    from .views import views
    from .auth import auth


    #This imports all the models before the database is created
    from .models import User, Post

    db.init_app(app)

    # this is needed in order for database session calls (e.g. db.session.commit)
    with app.app_context():
      try:
          db.create_all()
      except Exception as exception:
          print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
      finally:
          print("db.create_all() in __init__.py was successfull - no exceptions were raised")



    #Allows user to login and out
    #Allows user to access specific webpages if logged in 
    login_manager = LoginManager()
    login_manager.init_app(app)
    #Incase someone tries to access a page when they're not logged in
    #They get redirect to this page
    login_manager.login_view = 'auth.login'

    #This is known as a Session is like storage for your data, like not having to constantly login etc. 
    @login_manager.user_loader
    def load_user(id):
        #Double check query
        #Allows me to access information of user based on their ID
        #User (model), we are trying to find something (query)
        #and we are (get)ting the user object that has an ID equal to this ID
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app



