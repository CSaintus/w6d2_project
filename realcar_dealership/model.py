from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid
from flask_marshmallow import Marshmallow


from.helpers import get_image_url

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


@login_manager.user_loader
def load_user(user_id):
    """Given *user_id*, return the associated User object.
    :param user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    """User model."""  
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, first_name, last_name, email, password, username):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.username = username
        self.user_id = self.set_id()

    def set_id(self):
        return str(uuid.uuid4())


    def get_id(self):
        return str(self.user_id)


    def set_password(self, password):
        return generate_password_hash(password)


    def __repr__(self):
        return f"<User: {self.username}>"



class Car(db.Model):
    """Car model."""
    car_id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    transmission = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('cars', lazy=True))
    image_url = db.Column(db.String(1000), nullable=False)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False, default=1)


    def __init__(self, make, model, year, mileage, transmission, color, price, description, user_id, image_url):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.transmission = transmission
        self.color = color
        self.price = price
        self.description = description
        self.user_id = user_id
        self.image_url = self.set_image_url(image_url)
        self.car_id = self.set_id()
        self.date_modified = datetime.utcnow()
        self.quantity = quantity


    def set_id(self):
        return str(uuid.uuid4())

    def set_image_url(self, image_url):
        if not image_url:
            return 'https://www.publicdomainpictures.net/pictures/280000/velka/not-found-image-15383864787lu.jpg'
        else:
            return image_url

    def decrement_quantity(self, quantity):

        self.quantity -= int(quantity)
        return self.quantity

    def increment_quantity(self, quantity):
        self.quantity += int(quantity)
        return self.quantity

    def __repr__(self):
        return f"<Car: {self.make} {self.model}>"



class CarSchema(ma.Schema):
    """Marshmallow schema for Car."""
    class Meta:
        fields = ('car_id','make','model', 'year','mileage', 'transmission', 'color', 'price', 'description', 'user_id', 'image_url', 'date_modified', 'quantity')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)