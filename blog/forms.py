from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from blog.models import User
from flask_login import current_user
from flask_wtf.file import FileAllowed,FileField
# User Register Form
class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(),Length(min=2,max=35)])
    email = StringField("E-Mail:", validators=[DataRequired(),Email(message="Please enter a valid e-mail.")])
    password = PasswordField("Password:",validators=[DataRequired()])
    confirm_password = PasswordField("Verify password",validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("The username is already taken. Choose another one.")

    def validate_email(self,email):
        email = User.query.filter_by(email = email.data).first()
        if email:
            raise ValidationError("The email is already taken. Choose another one.")

# User Login Form
class LoginForm(FlaskForm):
    email = StringField("Email:",validators=[DataRequired(),Email()])
    password = PasswordField("Password:",validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

# Article Form
class ArticleForm(FlaskForm):
    title = StringField("Article Title", validators=[DataRequired()])
    content = TextAreaField("Article Content",validators=[DataRequired()])
    submit = SubmitField("Post")
# UpdateAccount Form
class UpdateAccount(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(),Length(min=2,max=35)])
    email = StringField("E-Mail:", validators=[DataRequired(),Email(message="Please enter a valid e-mail.")])
    picture = FileField("Update Profile Picture",validators=[FileAllowed(["jpg","png"])])
    submit = SubmitField("Update")

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("The username is already taken. Choose another one.")
    def validate_email(self,email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()
            if email:
                raise ValidationError("The email is already taken. Choose another one.")