from classes import User, Order, Offer
from data import users, orders, offers
from datetime import datetime
from classes import db


def check_keys(data: dict, keys: set) -> bool:
    """Проверяем ключи на валидность"""
    for key in data:
        if key not in keys:
            return False
    else:
        return True


def insert_data():
    new_users = []
    for user in users:
        new_users.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_users)

    new_orders = []

    for order in orders:
        new_orders.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.strptime(order['start_date'], '%m/%d/%Y'),
                end_date=datetime.strptime(order['end_date'], '%m/%d/%Y'),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_orders)

    new_offers = []
    for offer in offers:
        new_offers.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id'],
            )
        )
        with db.session.begin():
            db.session.add_all(new_offers)
