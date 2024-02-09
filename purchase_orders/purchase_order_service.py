from flask_restful import reqparse

from exceptions.exceptions import NotFoundValue
from exceptions.exceptions import QuantityException

from purchase_orders.models import PurchaseOrderModel
from db import db


class PurchaseOrderSevice:

    def _validate_quantity(self, quantity: int):
        if quantity < 50 or quantity > 150:
            raise QuantityException('The quantity must be between 50 and 150')

    def list_purchase_orders(self):
        purchase_orders = PurchaseOrderModel.query.all()
        return [p.as_dict() for p in purchase_orders]

    def add_purchase_order(self, kwargs: reqparse.Namespace):
        purchase_orders = PurchaseOrderModel(**kwargs)
        quantity = purchase_orders.as_dict()
        self._validate_quantity(quantity['quantity'])
        db.session.add(purchase_orders)
        db.session.commit()

        return purchase_orders.as_dict()

    def find_purchase_by_id(self, search: int):
        purchase_order = PurchaseOrderModel.query.filter_by(id=search).first()
        if not purchase_order:
            raise NotFoundValue("Purchase not Found")

        return purchase_order.as_dict()

    def delete_purchase_order(self, search: int):
        purchase_order = PurchaseOrderModel.query.filter_by(id=search).first()
        db.session.delete(purchase_order)
        db.session.commit()

        return purchase_order.as_dict()
