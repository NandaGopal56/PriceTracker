from flask_mail import Message
from flask import url_for
from app import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='pricetracker.info@gmail.com', recipients=[user.email])

    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not made this request then simply ignore this message. No changes will be made.
Thank you. 
'''

    mail.send(msg)