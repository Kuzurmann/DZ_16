import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from datetime import datetime
from utils import check_keys, insert_data
from classes import db, app
from classes import User, Order, Offer


def main():
    db.create_all()
    insert_data()
    app.run(debug=True)


@app.route('/orders/', methods=['GET', 'POST'])
def orders_index():
    if request.method == 'GET':
        data = []
        for order in Order.query.all():
            customer = User.query.get(order.customer_id).first_name if User.query.get(
                order.customer_id) else order.customer_id
            executor = User.query.get(order.executor_id).first_name if User.query.get(
                order.executor_id) else order.executor_id
            data.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": customer,
                "executor_id": executor,
            })
        return jsonify(data)

    elif request.method == 'POST':
        data = request.json()
        allowed_keys = {'name', 'description', 'start_date', 'end_date', 'address', 'price', 'customer_id',
                        'executor_id'}
        if check_keys(data, allowed_keys):
            new_order = Order(
                name=data.get('name'),
                description=data.get('description'),
                start_date=datetime.strptime(data['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(data['end_date'], '%m/%d/%Y'),
                address=data.get('address'),
                price=data.get('price'),
                customer_id=data.get('customer_id'),
                executor_id=data.get('executor_id')
            )

            with db.session.begin():
                db.session.add(new_order)

        print(Order.query.filter(Order.name == 'query').first())

        return "Новый заказ добавлен в базу!"


@app.route('/users/', methods=['GET', 'POST'])
def users_index():
    if request.method == 'GET':
        data = []
        for user in User.query.all():
            data.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone,

            })
        return jsonify(data)


    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone']
        )

        with db.session.begin():
            db.session.add(new_user)


    return "Новый пользователь добавлен в базу!"


@app.route('/offers/', methods=['GET', 'POST'])
def offers_index():
    if request.method == 'GET':
        data = []
        for offer in Offer.query.all():
            data.append({
                'id': offer.id,
                'order_id': offer.order_id,
                'executor_id': offer.executor_id

            })
        return jsonify(data)


    elif request.method == 'POST':
        data = request.json
        allowed_keys = {'order_id', 'executor_id'}
        if check_keys(data, allowed_keys):
            new_offer = Offer(
                order_id=data.get('order_id'),
                executor_id=data.get('executor_id')
            )
            with db.session.begin():
                db.session.add(new_offer)
            return 'Новое предложение успешно добавлено в базу!'


@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def orders_by_oid(oid):
    if request.method == 'GET':
        order = Order.query.get(oid)
        data = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id,
        }
        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        order = Order.query.get(oid)
        order.name = 'new_order'
        order.description = data['description']
        order.start_date = datetime.strptime(data['start_date'], '%m/%d/%Y')
        order.end_date = datetime.strptime(data['end_date'], '%m/%d/%Y')
        order.address = data['address']
        order.price = data['price']
        order.customer_id = data['customer_id']
        order.executor_id = data['executor_id']

        with db.session.begin():
            db.session.add(order)

        print(Order.query.filter(Order.name == 'new_order').first().name)

        return '', 203

    elif request.method == 'DELETE':
        order = Order.query.get(oid)
        db.session.delete(order)
        db.session.commit()


@app.route('/users/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def users_by_oid(oid):
    if request.method == 'GET':
        data = {}
        user = User.query.get(oid)
        data = {

            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone,

        }
        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        user = User.query.get(oid)
        user.first_name = 'first_name'
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        with db.session.begin():
            db.session.add(user)

        return '', 203

    elif request.method == 'DELETE':
        user = User.query.get(oid)
        db.session.delete(user)
        db.session.commit()


@app.route('/offers/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def offers_by_oid(oid):
    if request.method == 'GET':
        offer = Offer.query.get(oid)
        data = {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id,

        }
        return jsonify(data)

    elif request.method == 'PUT':
        data = request.get_json()
        offer = Offer.query.get(oid)
        offer.order_id = 'order_id'
        offer.executor_id = data['executor_id']

        with db.session.begin():
            db.session.add(offer)

        return '', 203

    elif request.method == 'DELETE':
        offer = Offer.query.get(oid)
        db.session.delete(offer)
        db.session.commit()


if __name__ == '__main__':
    main()
