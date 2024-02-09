import pytest

from purchase_orders.purchase_order_service import PurchaseOrderSevice
from purchase_orders.models import PurchaseOrderModel
from db import db
from exceptions.exceptions import NotFoundValue, QuantityException


def test_check_quantity_less_then_miminum(test_client):
    with pytest.raises(QuantityException) as ex:
        PurchaseOrderSevice()._validate_quantity(30)
    assert ex.value.code == 400
    assert ex.value.description == 'The quantity must be between 50 and 150'


def test_check_quantity_max_then_miminum(test_client):
    with pytest.raises(QuantityException) as ex:
        PurchaseOrderSevice()._validate_quantity(200)
    assert ex.value.code == 400
    assert ex.value.description == 'The quantity must be between 50 and 150'


def test_add_purchase_order(test_client):
    obj = {'description': 'Purchase Order id 2', 'quantity': 150}

    _service = PurchaseOrderSevice()

    _service.add_purchase_order(obj)

    purchase_on_db = PurchaseOrderModel.query.all()

    assert len(purchase_on_db) == 1
    assert purchase_on_db[0].id is not None
    assert purchase_on_db[0].description == 'Purchase Order id 2'
    assert purchase_on_db[0].quantity == 150

    db.session.query(PurchaseOrderModel).delete()
    db.session.commit()


def test_list_purchase_orders(test_client, purchase_on_db):
    _service = PurchaseOrderSevice()

    purchase_order = _service.list_purchase_orders()

    assert purchase_order[0]['id'] == purchase_on_db[0].id
    assert purchase_order[0]['description'] == purchase_on_db[0].description
    assert purchase_order[0]['quantity'] == purchase_on_db[0].quantity
    assert purchase_order[1]['id'] == purchase_on_db[1].id
    assert purchase_order[1]['description'] == purchase_on_db[1].description
    assert purchase_order[1]['quantity'] == purchase_on_db[1].quantity


def test_list_purchase_orders_by_id(test_client, purchase_on_db):
    _service = PurchaseOrderSevice()

    purchase_order = _service.find_purchase_by_id(purchase_on_db[0].id)

    assert purchase_order['id'] == purchase_on_db[0].id


def test_list_purchase_orders_invalid_id(test_client):

    with pytest.raises(NotFoundValue) as ex:
        PurchaseOrderSevice().find_purchase_by_id(-1)
    assert ex.value.code == 400
    assert ex.value.description == 'Purchase not Found'


def test_delete_purchase_order(test_client):
    _service = PurchaseOrderSevice()

    purchase_order = PurchaseOrderModel(description='Purchase Order id 3', quantity=150)
    db.session.add(purchase_order)
    db.session.commit()

    _service.delete_purchase_order(purchase_order.id)

    purchase_order = PurchaseOrderModel.query.first()

    assert purchase_order is None
