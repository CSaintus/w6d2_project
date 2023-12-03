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


class customer(db.Model):
    """Customer model."""
    customer_id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    carorder_id = db.relationship('Carorder', backref=db.backref('customer', lazy=True))

    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.date_added = datetime.utcnow()

    def __repr__(self):
        return f"<Customer: {self.customer_id}>"




class Carorder(db.Model):
    """Carorder model."""
    carorder_id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    car = db.relationship('Car', backref=db.backref('carorder', lazy=True))
    customer = db.relationship('customer', backref=db.backref('carorder', lazy=True))


    def __init__(self, car_id, customer_id, quantity, price, date_added, date_modified):
        self.car_id = car_id
        self.customer_id = customer_id
        self.quantity = quantity
        self.price = price
        self.date_added = date_added
        self.date_modified = date_modified
        self.carorder_id = self.set_id()


    def set_id(self):
        return str(uuid.uuid4())

    def set_price(self, quantity, price):

        quantity = int(quantity)
        price = float(price)

        self.price = quantity * price
        return self.price

    def update_quantity(self, quantity):
        self.quantity = quantity
        return self.quantity


    class Order(db.Model):
        order_id = db.Column(db.Integer, primary_key=True)
        order_total = db.Column(db.Integer, nullable=False)
        date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
        carorder_id = db.relationship('Carorder', backref=db.backref('order', lazy=True))


        def __init__(self, order_total, date_added, carorder_id):
            self.order_total = order_total
            self.date_added = date_added
            self.carorder_id = carorder_id
            self.order_id = self.set_id()

        def set_id(self):
            return str(uuid.uuid4())


        def increment_order_total(self, order_total):

            self.order_total += float(order_total)
            return self.order_total


        def decrement_order_total(self, order_total):
            self.order_total -= float(order_total)
            return self.order_total


        def __repr__(self):
            return f"<Order: {self.order_id}>"


class CarSchema(ma.Schema):
    """Marshmallow schema for Car."""
    class Meta:
        fields = ('car_id','make','model', 'year','mileage', 'transmission', 'color', 'price', 'description', 'user_id', 'image_url', 'date_modified', 'quantity')


car_schema = CarSchema()
cars_schema = CarSchema(many=True)