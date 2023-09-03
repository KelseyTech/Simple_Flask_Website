from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 

#db.model is basically a table (rows are the users)(columns have information of users)
#This class is defining columns in our user table
class User(db.Model, UserMixin):
    #Primary key is needed in all tables almost always an integer 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(50))
    #func just means it'll use the current time
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    #This references all the 'Posts' that the user has 
    #back ref gives access to all the user data when getting 
    posts = db.relationship('Post', backref='user', passive_deletes=True)
    comments = db.relationship('Comments', backref='user', passive_deletes=True)
    


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"), nullable=False)





    
    
