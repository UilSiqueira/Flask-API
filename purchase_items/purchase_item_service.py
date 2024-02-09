from flask import jsonify
from flask_restful import reqparse

from db import db
from purchase_items.models import PurchaseItemsModel
from purchase_orders.models import PurchaseOrderModel
from exceptions.exceptions import QuantityException


class PurchaseItemService:

    def _check_maximum_purchase_order_quantity(self, purchase_order_id: int,
                                               purchase_order_quantity: int,
                                               quantity: int):
        purchase_orders_items = PurchaseItemsModel.query.filter_by(purchase_order_id=purchase_order_id).all()

        sum_items = 0
        for item in purchase_orders_items:
            sum_items += item.quantity

        if (sum_items + quantity) > purchase_order_quantity:
            allowed_quantity = (purchase_order_quantity - sum_items)
            raise QuantityException(f'You can add only {allowed_quantity} more items')

    def add_purchase_item(self, kwargs: reqparse.Namespace):
        purchase_order_id = kwargs['purchase_order_id']
        purchase_order = PurchaseOrderModel.query.filter_by(id=purchase_order_id).first()
        if purchase_order:
            self._check_maximum_purchase_order_quantity(
                purchase_order.id, purchase_order.quantity, kwargs['quantity'])
            purchase_item = PurchaseItemsModel(**kwargs)

            db.session.add(purchase_item)
            db.session.commit

            item = PurchaseItemsModel.query.filter_by(purchase_order_id=purchase_order_id).first()

            return item.as_dict()

        return jsonify({'message': f'Order id {purchase_order_id} not found'})

    def list_items_by_purchase_id(self, search: int):
        purchase_order = PurchaseOrderModel.query.filter_by(id=search).first()
        if purchase_order:
            items = PurchaseItemsModel.query.filter_by(purchase_order_id=search).all()
            return [item.as_dict() for item in items]

        return jsonify({'message': f'Purchase order id {search} not found'})

    def delete_item_by_purchase_id(self, order_id: int, item_id: int):
        purchase_order = PurchaseOrderModel.query.filter_by(id=order_id).first()
        if purchase_order:
            item = PurchaseItemsModel.query.filter_by(id=item_id).first()
            if item:
                db.session.delete(item)
                db.session.commit()
                return
            return jsonify({'message': f'Item id {item_id} not found'})
        return jsonify({'message': f'Order id {order_id} not found'})
