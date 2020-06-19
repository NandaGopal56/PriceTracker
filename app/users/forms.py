from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo,ValidationError
from app.db import User

#register form
class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=3,max=25)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=5,max=25)])
    confirm_password = PasswordField('confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken !! please choose a different one')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken !! please choose a different one')

#signin form
class SigninForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


#form for request to reset password
class RequestResetForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is None:
            raise ValidationError('There is no account with this email. You must register first !!')

#form for reseting password
class ReserPasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Length(min=5,max=25)])
    confirm_password = PasswordField('confirm_Password',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')