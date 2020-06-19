from flask import Blueprint
from flask import render_template, url_for, flash, redirect
from app.posts.forms import DetailsForm
from flask_login import  current_user


main = Blueprint('main','__name__')

first_time_access = True
@main.route('/',methods=['GET','POST'])
@main.route('/index',methods=['GET','POST'])
def index():
    global first_time_access
    if current_user.is_authenticated:
        if first_time_access:
            flash(f'You are already logged in !!','success')
            first_time_access = False
        return redirect(url_for('posts.access'))
    else:
        form = DetailsForm()
        if form.validate_on_submit():
            return redirect(url_for('posts.access'))

    return render_template("index.html",title="Price Tracker-Home",form=form)


@main.route("/about")
def about():
    return render_template('about.html',title='About Us')