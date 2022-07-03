import datetime
import data
from models import *


db.drop_all()

db.create_all()


for user in data.USERS:
    db.session.add(User(
        id=user["id"],
        first_name=user["first_name"],
        last_name=user["last_name"],
        age=user["age"],
        email=user["email"],
        role=user["role"],
        phone=user["phone"]
    ))

for order in data.ORDERS:
    started_month, started_day, started_year = order["start_date"].split('/')
    ended_month, ended_day, ended_year = order["end_date"].split('/')
    start_month = int(started_month)
    start_day = int(started_day)
    start_year = int(started_year)
    end_month = int(ended_month)
    end_day = int(ended_day)
    end_year = int(ended_year)
    db.session.add(Order(
        id=order["id"],
        name=order["name"],
        description=order["description"],
        start_date=datetime.date(year=start_year, month=start_month, day=start_day),
        end_date=datetime.date(year=end_year, month=end_month, day=end_day),
        address=order["address"],
        price=order["price"],
        customer_id=order["customer_id"],
        executor_id=order["executor_id"]
    ))


for offer in data.OFFERS:
    db.session.add(Offer(
        id=offer["id"],
        order_id=offer["order_id"],
        executor_id=offer["executor_id"]
    ))

db.session.commit()
