from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from .purchase_item_service import PurchaseItemService


class PurchaseOrdersItems(Resource):
    _service = PurchaseItemService()
    parser = reqparse.RequestParser()
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='Inform a valid description'
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='Inform a valid price'
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help='Inform a valid quantity'
    )

    @jwt_required()
    def get(self, id: int):
        return self._service.list_items_by_purchase_id(id)

    @jwt_required()
    def post(self, id: int):
        data = PurchaseOrdersItems.parser.parse_args()
        data['purchase_order_id'] = id
        return self._service.add_purchase_item(data)


class PurchaseDeleteOrdersItems(Resource):
    _service = PurchaseItemService()

    @jwt_required()
    def delete(self, order_id: int, item_id: int):
        return self._service.delete_item_by_purchase_id(order_id, item_id)
