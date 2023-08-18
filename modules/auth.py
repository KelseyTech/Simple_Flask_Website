#Routes for users logged in
from flask import Blueprint, render_template, flash, request , redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User 

auth = Blueprint('auth', __name__)


#------------------
#---Sign-Up-Page---
#------------------
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #This is how we get the data from the form
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        print(password1)

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        
        #Checks all the possible errors
        if email_exists:
            flash("Email already exist", category='error')
        elif username_exists:
            flash("Username taken", category='error')
        elif password1 != password2:
            flash("Password Don't match", category='error')
        elif len(username) < 2:
            flash("Username too short", category='error')
        elif len(password1) < 6:
            flash("Password too short", category='error')
        #Creates the new user 
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return render_template('sign_success.html')

    return render_template('signUp.html', user=current_user)


#--------------------------
#---Sign-Up-Page-Success---
#--------------------------
@auth.route('sign_yes', methods=['GET'])
def sign_yes():
    return render_template('sign_success.html')


#------------------
#----Login-Page----
#------------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password1")

        user = User.query.filter_by(email=email).first()
        #This checks if the email is associated with an account
        if user:
            #This checks the hashed password with the one written
            if check_password_hash(user.password, password):
                flash('Logged in', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect', category="error")
        else:
            flash('User does not exist')

    return render_template('login.html', user=current_user)



#------------------
#---Logout-Page----
#------------------
#This makes it so you can only access this page if you're logged in 
#login_user is required to access this page 
@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('views.home'))