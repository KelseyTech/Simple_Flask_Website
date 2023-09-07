# Routes for users not logged in
from flask import (Blueprint, render_template, render_template_string, request, flash,redirect, url_for)
from flask_login import login_required, current_user

from . import db
from .models import Post, User, Comment

views = Blueprint("views", __name__)


# -------------------------
# -------------------------
# --------Home-Page--------
# -------------------------
# -------------------------

@views.route("/")
@views.route("/home")
@login_required
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)



# -------------------------
# -------------------------
# ------Create-Post--------
# -------------------------
# -------------------------

@views.route("/home", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")

        if not text:
            flash("Post cannot be empty", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created!", category="success")

    return redirect(url_for("views.home", user=current_user))



# -------------------------
# -------------------------
# ------Add-Comment--------
# -------------------------
# -------------------------

@views.route("/create-comment/<post_id>", methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty.', category='error')
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(
                text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist.', category='error')

    return redirect(url_for('views.home'))



# -------------------------
# -------------------------
# ------Remove-Comment-----
# -------------------------
# -------------------------

@views.route("/delete-comment/<comment_id>")
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()

    if not comment:
        flash('Comment does not exist.', category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author:
        flash('You do not have permission to delete this comment.', category='error')
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for('views.home'))











# -------------------------
# -------------------------
# -------Delete-Post-------
# -------------------------
# -------------------------

@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()

    if not post:
        flash("Post does not exist.", category="error")
    elif current_user.id != post.author:
        flash("You do not have permission to delete this post.", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.", category="success")
    return redirect(url_for("views.home"))


# -------------------------
# -------------------------
# -----Profile--Page-------
# -------------------------
# -------------------------
@views.route("/user/<username>", methods=["GET", "POST"])
@login_required
def profile(username):

    #Allows user to create a post on their profile 
    create_post()

    #Checks if user exists
    user = User.query.filter_by(username=username).first()
    if not user:
        flash("User does not exist", category="error")
        return redirect(url_for("views.home"))
    
    #Grabs all the users posts 
    post = Post.query.filter_by(author=user.id).all()

    #Counts the number of posts the user has
    post_number = len(post)

    return render_template("user.html", user=current_user, username=username, posts=post, post_number=post_number)
