from flask import Blueprint
from app import bcrypt
from flask import render_template, url_for, flash, redirect, request
from app.users.forms import RegistrationForm , SigninForm, RequestResetForm, ReserPasswordForm
from app.db import db, User,Information
from flask_login import login_manager, login_user, current_user, logout_user, login_required
from app import scrape, mail
from flask_mail import Message
import time
from app.users import utils

users = Blueprint('users','__name__')

########################################################################################################################
@users.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.access'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'your account has been created successfully !! Your username is {form.username.data}!','success')
        return redirect(url_for('users.signin'))

    return render_template("register.html",title="Price Tracker-Register",form=form)
########################################################################################################################
@users.route('/signin',methods=['GET','POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('posts.access'))    

    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'You are logged in successfully','success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('posts.access'))
        else:
            flash(f'login unsuccessful please check email and password','danger')
    return render_template("signin.html",title="Price Tracker-Sign In",form=form)

########################################################################################################################
@users.route("/signout")
def signout():
    logout_user()
    flash(f'You have been logged out successfully','danger')
    return redirect(url_for('main.index'))

########################################################################################################################
@users.route("/request_password",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('posts.access'))
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        utils.send_reset_email(user)
        flash('An email with a link has been sent to reset the password','info')
        return redirect(url_for('users.signin'))
    return render_template('reset_request.html',title='Price Tracker-Reset Password',form=form)

########################################################################################################################
@users.route("/request_password/<token>",methods=['GET','POST'])
def reset_token(token=10):
    if current_user.is_authenticated:
        return redirect(url_for('posts.access'))
    user = User.verify_reset_token(token)
    form = ReserPasswordForm()

    if user is None:
        flash('That is an invalid or expired token','warning')
        return redirect(url_for('users.reset_request'))
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'your password has been updated !!','success')
        return redirect(url_for('users.signin'))

    return render_template('reset_token.html',title='Price Tracker-Reset Password',form=form)

########################################################################################################################
@users.route('/history',methods=['GET','POST'])
@login_required
def history():
    
    user = User.query.filter_by(email=current_user.email).first()
    posts = user.info
    if request.method == 'POST':
        info_id = request.form.get('delete')
        Information.query.filter_by(info_id=info_id).delete()
        db.session.commit()
        return redirect(url_for('users.history'))
    
    return render_template('history.html',title='Account',posts=posts)