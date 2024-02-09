from decouple import config
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db

from purchase_items.resources import PurchaseOrdersItems, PurchaseDeleteOrdersItems
from purchase_orders.resources import PurchaseOrders, PurchaseOrderById
from users.resources import UserCreation, UserLogin


def create_app():
    app = Flask(__name__)
    api = Api(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = config('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = config('JWT_SECRET_KEY')

    db.init_app(app)

    Migrate(app, db)

    JWTManager(app)

    api.add_resource(PurchaseOrders, '/purchase_orders')
    api.add_resource(PurchaseOrderById, '/purchase_orders/<int:id>')
    api.add_resource(PurchaseOrdersItems, '/purchase_orders/<int:id>/items')
    api.add_resource(PurchaseDeleteOrdersItems, '/purchase_orders/<int:order_id>/items/<int:item_id>')
    api.add_resource(UserCreation, '/users')
    api.add_resource(UserLogin, '/login')

    @app.before_request
    def create_tables():
        db.create_all()

    return app
