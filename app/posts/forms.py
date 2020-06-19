from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from app.db import User


#form to get the product url and target price
class DetailsForm(FlaskForm):
    link = StringField('Enter Product URL',validators=[DataRequired()])
    target_price = StringField('Enter your Target Price',validators=[DataRequired()])
    submit = SubmitField('Submit')
