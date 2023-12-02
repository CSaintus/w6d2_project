from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, decimalField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')



class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('<CONFIRM PASSWORD>', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class AddCarForm(FlaskForm):
    make = StringField('Make', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired()])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Add Car')
    image = StringField('Img url **(optional)')
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    description = StringField('Description **(optional)')