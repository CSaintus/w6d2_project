from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from realcar_dealership.models import customer, car, carorder, order, db, cars_schema, orders_schema, customers_schema


api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/token', methods=['GET', 'POST'])
def token():

    data = request.json
    if data:
        client_id = data['client_id']
        access_token = create_access_token(identity=client_id)
        return{
            'access_token': access_token,
        }
    else:
        return{
            'error': 'No data was provided',
        }


@api.route('/cars')
@jwt_required()
def get_cars():

    allcars = car.query.all()
    response = cars_schema.dump(allcars)
    return jsonify(response)


@api.route('/order/add/<customer_id>', methods=['POST'])
@jwt_required()
def order_car(customer_id):

    data = request.json
    
    customer_order = data['order']

    customer = customer.query.filter_by(id=customer_id).first()
    if not customer:
        customer = customer(customer_order['name'], customer_order['email'], customer_order['phone'])
        db.session.add(customer)

    order = order()
    db.session.add(order)

    for car in customer_order['cars']:

        carorder = carorder(car_id, order.id, car['quantity'], car['price'], customer.id)
        db.session.add(carorder)


        order.increment_total(car['quantity'], car['price'])

        current_car = car.query.get(car['id'])
        current_car.decrement_quantity(car['quantity'])

    db.session.commit()

    return{
        'status' : 200,
        'message' : 'Order placed successfully',
    }

    @api.route('/add/<customer_id>')
    @jwt_required()
    def get_order(customer_id):

        carorders = carorder.query.filter_by(customer_id=customer_id).all()


        data = []

        for order in carorders:

            car = car.query.get(Car.car_id == car.car.id).first()

            car_dict = car_schema.dump(car)

            car_dict['quantity'] = order.quantity
            car_dict['order_id'] = order.order_id
            car_dict['id'] = order.carorder_id

            data.append(car_dict)

        return jsonify(data)

    @api.route('/order/update/<order_id>', methods=['PUT'])
    @jwt_required()
    def update_order(order_id):

        data = request.json
        new_quantity = int(data['quantity'])
        car_id = data['car_id']

        carorder = carorder.query.filter_by(Carorder.order_id == order_id, CarOrder.car_id == car_id).first()
        order = order.query.get(order_id)
        car = car.query.get(car_id)


        carorder.set_price(car.price, new_quantity)

        diff = abs(new_quantity - carorder.quantity)

        if carorder.quantity > new_quantity:
            car.increment_quantity(diff)
            order.decrement_total(diff, car.price)

        elif carorder.quantity < new_quantity:
            car.decrement_quantity(diff)
            order.increment_total(diff, car.price)

        carorder.update_quantity(new_quantity)
        db.session.commit()

        return{
            'status' : 200,
            'message' : 'Order updated successfully'
        }

    @api.route('/order/delete/<order_id>', methods=['DELETE'])
    @jwt_required()
    def delete_order(order_id):

        data = request.json
        car_id = data['car_id']

        carorder = carorder.query.filter_by(Carorder.order_id == order_id, CarOrder.car_id == car_id).first()
        order = order.query.get(order_id)
        car = car.query.get(car_id)

        order.decrement_total(carorder.quantity, car.price)
        car.increment_quantity(carorder.quantity)

        db.session.delete(carorder)
        db.session.commit()

        return{
            'status' : 200,
            'message' : 'Order deleted successfully'
        }
