from flask import render_template, url_for, flash, redirect,request
from blog.models import User, Post
from blog.forms import RegisterForm,LoginForm
from blog import app, db, bcrypt
from flask_login import login_user,current_user,logout_user,login_required

posts = [
        {
            'author' : 'Abdullah Kartal',
            'title': 'Article 1',
            'content' : 'First Article Content',
            'date_posted' : '21 July 2018'
        },
{
            'author' : 'Suleyman Cakir',
            'title': 'Article 2',
            'content' : 'Second Article Content',
            'date_posted' : '22 July 2018'
            }
]
# Index
@app.route("/")
def index():
    return render_template("index.html",posts = posts)
# About
@app.route("/about")
def about():
    return render_template("about.html",title = 'About')
# Register
@app.route("/register",methods=["GET","POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashpass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data, password = hashpass)
        db.session.add(user)
        db.session.commit()
        flash("You are successfully registered..","success")
        return redirect(url_for("login"))
    return render_template("register.html",title = "Register",form=form)
# Login
@app.route("/login",methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next = request.args.get("next")
            flash ("You are successfully log in.","success")
            return redirect(next) if next else redirect(url_for("index"))
        else:
            flash("Check your email or password.","danger")
    return render_template("login.html",title = "Login",form=form)

# Logout
@app.route("/logout")
def logout():
    logout_user()
    flash("You are successfully log out","success")
    return redirect(url_for("index"))

# Account
@app.route("/account")
@login_required
def account():
    return render_template("account.html",title = "Account")
