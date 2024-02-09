import pytest

from purchase_orders.models import PurchaseOrderModel
from purchase_items.models import PurchaseItemsModel
from purchase_items.purchase_item_service import PurchaseItemService
from exceptions.exceptions import QuantityException


def test_check_maximum_purchase_order_quantity(test_client, purchase_items_on_db):
    purchase_order_id = purchase_items_on_db['purchase_order']['id']
    purchage_order_quantity = purchase_items_on_db['purchase_order']['quantity']
    item_quantity = 300

    with pytest.raises(QuantityException) as ex:
        PurchaseItemService()._check_maximum_purchase_order_quantity(purchase_order_id,
                                                                     purchage_order_quantity,
                                                                     item_quantity)

    assert ex.value.code == 400
    assert ex.value.description == 'You can add only 100 more items'


def test_add_purchase_item(test_client, purchase_on_db):

    _service = PurchaseItemService()

    item_obj = {
        'description': 'Item teste',
        'price': 10.0,
        'quantity': 5
    }

    item_obj['purchase_order_id'] = purchase_on_db.id
    _service.add_purchase_item(item_obj)

    items_on_db = PurchaseItemsModel.query.all()

    assert len(items_on_db) == 1
    assert items_on_db[0].id is not None
    assert items_on_db[0].description == item_obj['description']
    assert items_on_db[0].price == item_obj['price']
    assert items_on_db[0].quantity == item_obj['quantity']


def test_list_items_by_purchase_id(test_client, purchase_items_on_db):

    _service = PurchaseItemService()

    purchase_on_db = PurchaseOrderModel.query.all()

    items = _service.list_items_by_purchase_id(purchase_on_db[0].id)

    assert items == purchase_items_on_db['items']


def test_delete_purchase_item(test_client,  purchase_items_on_db):

    _service = PurchaseItemService()

    first_item = 0
    item_order_id = purchase_items_on_db['items'][first_item]['id']
    purchase_order_id = purchase_items_on_db['purchase_order']['id']

    _service.delete_item_by_purchase_id(purchase_order_id, item_order_id)

    deleted_item = PurchaseItemsModel.query.filter_by(id=item_order_id).first()

    assert deleted_item is None
