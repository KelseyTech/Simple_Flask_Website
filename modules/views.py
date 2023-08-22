# Routes for users not logged in
from flask import Blueprint, render_template, render_template_string, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db  
from .models import Post, User

views = Blueprint("views", __name__)


#------------------
#----Home-Page-----
#------------------
@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


#------------------
#---Create-Post----
#------------------
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created!', category='success')
            return redirect(url_for('views.home'))

    return render_template('create_post.html', user=current_user)



#------------------
#---Delete-Post----
#------------------
@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category='error')
    elif current_user.id != post.author:
        flash('You do not have permission to delete this post.', category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.home'))

#------------------
#--Profile--Page---
#------------------
@views.route('/user/<int:account_id>', methods=['GET', 'POST'])
@login_required
def user(account_id):
    get_user = User.query.filter_by(id=account_id).first()
    user_id = account_id
    print(account_id)
    return render_template('user.html', account_id=account_id)


