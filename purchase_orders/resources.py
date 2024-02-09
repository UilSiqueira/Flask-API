from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from purchase_orders.purchase_order_service import PurchaseOrderSevice


class PurchaseOrders(Resource):
    _service = PurchaseOrderSevice()

    parser = reqparse.RequestParser()
    parser.add_argument(
        'description',
        type=str,
        required=True,
        help='Inform a valid description'
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help='Inform a valid quantity'
    )

    @jwt_required()
    def get(self):
        return self._service.list_purchase_orders()

    def post(self):
        data = PurchaseOrders.parser.parse_args()
        return self._service.add_purchase_order(data)


class PurchaseOrderById(Resource):
    _service = PurchaseOrderSevice()

    @jwt_required()
    def get(self, id: int):
        return self._service.find_purchase_by_id(id)

    @jwt_required()
    def delete(self, id: int):
        return self._service.delete_purchase_order(id)
