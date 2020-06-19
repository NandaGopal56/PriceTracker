from flask import Blueprint
from app.db import  db
from flask import render_template, url_for, flash, redirect, request
from app.posts.forms import DetailsForm
from app.db import Information
from flask_login import login_manager, login_user, current_user, logout_user, login_required
from app import scrape


posts = Blueprint('posts','__name__')


@posts.route('/access',methods=['GET','POST'])
@login_required
def access():
    form = DetailsForm()

    if form.validate_on_submit():
        link = form.link.data
        target_price = form.target_price.data

        current_price = scrape.Get_details(link)

        if (current_price) :
            if target_price.isdigit():
                target_price = int(form.target_price.data)

                current_price = current_price[1:len(current_price)]
                price = ''
                check = ['0','1','2','3','4','5','6','7','8','9']
                for digit in str(current_price):
                    if digit in check:
                        price += digit
                    elif digit in ['!','@','#','$','%','^','&','*','~','.']:
                        break
                int_current_price = int(price)

                info = Information(author=current_user,email=current_user.email,link=link,current_price=int_current_price,new_price=int_current_price,target_price=target_price,status=True)
                db.session.add(info)
                db.session.commit()
                flash(f'your link is :   {link} ','success')
            else:
                flash(f'your target price should be a whole number','danger')
        else:
            flash(f'your product url is invalid. please provide a valid one !!','danger')
        
    return render_template("index.html",title="Price Tracker-Home",form=form)
