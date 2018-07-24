from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo

# User Register Form
class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(),Length(min=2,max=35)])
    email = StringField("E-Mail:", validators=[DataRequired(),Email(message="Please enter a valid e-mail.")])
    password = PasswordField("Password:",validators=[DataRequired()])
    confirm_password = PasswordField("Verify password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign Up")
# User Login Form
class LoginForm(FlaskForm):
    email = StringField("Email:",validators=[DataRequired(),Email()])
    password = PasswordField("Password:",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")
# Article Form
class ArticleForm(FlaskForm):
    title = StringField("Article Title", validators=[Length(min=5,max=100)])
    content = TextAreaField("Article Content",validators=[Length(min=10)])