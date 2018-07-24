from flask import render_template, url_for, flash, redirect
from blog.models import User, Post
from blog.forms import RegisterForm,LoginForm
from blog import app

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
    form = RegisterForm()
    if form.validate_on_submit():
        flash("You are successfully registered..","success")
        return redirect(url_for("index"))
    return render_template("register.html",title = "Register",form=form)
# Login
@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "abdullah@deneme.com" and form.password.data == "12345":
            flash("You are successfully log in","success")
            return redirect(url_for("index"))
        else:
            flash("Check your username or password.","danger")
    return render_template("login.html",title = "Login",form=form)