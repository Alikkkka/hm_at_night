from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from models import *
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


@app.route('/')
def show():
    return "Приветствую!"


@app.route('/users/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = []
        for user in User.query.all():
            result.append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
          id=user["id"],
          first_name=user["first_name"],
          last_name=user["last_name"],
          age=user["age"],
          email=user["email"],
          role=user["role"],
          phone=user["phone"]
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.close()

        return "Пользователь добавлен в БД!", 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_by_id(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Пользователь не найден!"
        else:
            return jsonify(user.to_dict())

    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.role = user_data['role']
        user.phone = user_data['phone']
        user.email = user_data['email']

        db.session.add(user)
        db.session.commit()
        return 'Данные о пользователе изменены!'

    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        db.session.delete(user)
        db.session.commit()
        return 'Пользователь удален!'


@app.route('/orders/', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        order = json.loads(request.data)
        started_month, started_day, started_year = order["start_date"].split('/')
        ended_month, ended_day, ended_year = order["end_date"].split('/')
        start_month = int(started_month)
        start_day = int(started_day)
        start_year = int(started_year)
        end_month = int(ended_month)
        end_day = int(ended_day)
        end_year = int(ended_year)
        new_order = Order(
            id=order["id"],
            name=order["name"],
            description=order["description"],
            start_date=datetime.date(year=start_year, month=start_month, day=start_day),
            end_date=datetime.date(year=end_year, month=end_month, day=end_day),
            address=order["address"],
            price=order["price"],
            customer_id=order["customer_id"],
            executor_id=order["executor_id"]
        )
        db.session.add(new_order)
        db.session.commit()
        db.session.close()
        return "Заказ добавлен в БД!", 200


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_by_id(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден!"
        else:
            return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_data = json.loads(request.data)
        order = db.session.query(Order).get(order_id)
        start_month, start_day, start_year = [int(i) for i in order["start_date"].split('/')]
        end_month, end_day, end_year = [int(i) for i in order["end_date"].split('/')]
        order.name = order_data['name']
        order.description = order_data['description']
        order.price = order_data['price']
        order.address = order_data['address']
        order.customer_id = order_data['customer_id']
        order.executor_id = order_data['executor_id']
        order.start_date = datetime.date(year=start_year, month=start_month, day=start_day)
        order.end_date = datetime.date(year=end_year, month=end_month, day=end_day)
        db.session.add(order)
        db.session.commit()
        return 'Данные о заказе изменены!'

    elif request.method == 'DELETE':
        order = db.session.query(Order).get(order_id)
        db.session.delete(order)
        db.session.commit()
        return "Заказ удален!"


@app.route('/offers/', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        offer = json.loads(request.data)
        new_offer = Offer(
            id=offer["id"],
            order_id=offer["order_id"],
            executor_id=offer["executor_id"]
        )
        db.session.add(new_offer)
        db.session.commit()
        db.session.close()

        return "Предложение добавлено в БД!", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено!"
        else:
            return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_data = json.loads(request.data)
        offer = db.session.query(Offer).get(offer_id)
        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']

        db.session.add(offer)
        db.session.commit()
        return 'Данные о предложении изменены!'

    elif request.method == 'DELETE':
        offer = db.session.query(Offer).get(offer_id)
        db.session.delete(offer)
        db.session.commit()
        return 'Предложение удалено!'


if __name__ == '__main__':
    app.run(debug=True, port=5009)


