from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,validators,PasswordField
from passlib.hash import sha256_crypt
from functools import wraps

# Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Please login for this page.","danger")
            return redirect(url_for("login"))
            
    return decorated_function
# User Register Form
class RegisterForm(Form):
    name = StringField("İsim:", validators=[validators.Length(min=4,max=32)])
    username = StringField("Kullanıcı Adı:", validators=[validators.Length(min=5,max=18)])
    email = StringField("Email Adresi:", validators=[validators.Email(message="Lütfen geçerli bir email giriniz.")])
    password = PasswordField("Şifrenizi giriniz:",validators=[
        validators.DataRequired("Lütfen bir parola giriniz:"),
        validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor.")
        ])
    confirm = PasswordField("Parola doğrula")
class LoginForm(Form):
    username = StringField("Kullanıcı Adı:")
    password = PasswordField("Parola:")
app = Flask(__name__)
app.secret_key = "akblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "akblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


# Register
@app.route("/register",methods = ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()

        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()

        cursor.close()
        flash("Başarıyla kayıt oldunuz.","success")
        
        return redirect(url_for("login"))
    else:
        return render_template("register.html",form = form)
'''
@app.route("/article/<string:id>")
def detail(id):
    return "Article id"+ id
'''
#Login
@app.route("/login",methods = ["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Select * From users where username = %s"
        
        result = cursor.execute(sorgu,(username,))
        if result > 0:
            data = cursor.fetchone()
            real_password = data ["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla giriş yaptınız.","success")
                session["logged_in"] = True
                session["username"] = username

                return redirect (url_for("index"))
            else:
                flash("Parolanızı kontrol ediniz.","danger")
                return redirect (url_for("login"))
        else:
            flash("Böyle bir kullanıcı bulunmuyor.","danger")
            return redirect (url_for("login"))

    return render_template("login.html",form = form)

# Logout

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
    