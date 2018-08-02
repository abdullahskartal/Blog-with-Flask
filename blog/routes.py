import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request,abort
from blog.models import User, Article
from blog.forms import RegisterForm,LoginForm,UpdateAccountForm,ArticleForm,RequestResetForm,ResetPasswordForm
from blog import app, db, bcrypt,mail
from flask_login import login_user,current_user,logout_user,login_required
from flask_mail import Message

# Index
@app.route("/")
def index():
    return render_template("index.html")

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

# Save picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,"static\\profile",picture_fn)
    
    output_size =(125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

# Account
@app.route("/account",methods = ["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit() 
        flash("Your account has been updated.","success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename = "profile/" + current_user.image_file)
    return render_template("account.html",title = "Account",image_file = image_file,form = form)

# Dashboard Page
@app.route("/dashboard")
@login_required
def dashboard():
    articles = Article.query.all()
    return render_template("dashboard.html",articles = articles)

# Add Article Page
@app.route("/addarticle",methods =["GET","POST"])
@login_required
def addarticle():
    form = ArticleForm()
    if form.validate_on_submit():
        article = Article(title=form.title.data, content = form.content.data, author = current_user)
        db.session.add(article)
        db.session.commit()
        flash("Your article has been created.","success")
        return redirect(url_for("dashboard"))
    return render_template("addarticle.html",title="New Article",form = form, legend = "New Article")

# Articles Page
@app.route("/articles")
@login_required
def articles():
    articles = Article.query.all()
    return render_template("articles.html",articles = articles)

# Article Page
@app.route("/article/<int:article_id>")
def article(article_id):
    article = Article.query.get_or_404(article_id)
    return render_template("article.html",title = article.title,article=article)

# Edit Article
@app.route("/edit/<int:article_id>",methods =["GET","POST"])
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        db.session.commit()
        flash("Your article has been successfully edited.","success")
        return redirect(url_for("article",article_id = article.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
    return render_template("addarticle.html",title="Edit Article",form = form, legend = "Edit Article")
    
# Delete Article
@app.route("/delete/<int:article_id>",methods =["POST","GET"])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash("Your article has been deleted.","success")
    return redirect(url_for("dashboard"))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",sender = "example@example.com",recipients=[user.email])
    msg.body = f''' If you want to reset your password click this link:
{url_for("reset_token",token = token, _external = True)}

If this mail is not in your information please just ignore.    
'''
    mail.send(msg)

# Reset Password
@app.route("/reset_password",methods = ["GET","POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash("Reset password email has been sent.","info")
        return redirect(url_for("login"))
    return render_template("reset_request.html",title = "Reset Password",form = form)

# Reset Password Token
@app.route("/reset_password/<token>",methods = ["GET","POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid token.","warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashpass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashpass
        db.session.commit()
        flash("Your password has been updated","success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title = "Reset Password",form = form)