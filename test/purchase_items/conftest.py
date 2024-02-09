import pytest
from db import db

from purchase_orders.models import PurchaseOrderModel
from purchase_items.models import PurchaseItemsModel


@pytest.fixture()
def purchase_on_db():

    purchase_obj = {'description': 'Purchase Order id 2', 'quantity': 200}
    purchase_order = PurchaseOrderModel(**purchase_obj)
    db.session.add(purchase_order)
    db.session.commit()

    db.session.refresh(purchase_order)

    yield purchase_order

    # Erase the foreign key
    db.session.query(PurchaseItemsModel).delete()
    db.session.query(PurchaseOrderModel).delete()

    db.session.commit()


@pytest.fixture()
def purchase_items_on_db():

    po = PurchaseOrderModel('Pedido de testes', 150)
    db.session.add(po)
    db.session.commit()

    poi_one = PurchaseItemsModel('Item 1', 10.89, 30, po.id)
    poi_two = PurchaseItemsModel('Item 2', 20.00, 20, po.id)

    items = [
        poi_one,
        poi_two
    ]

    for item in items:
        db.session.add(item)

    db.session.commit()

    for item in items:
        db.session.refresh(item)

    items_from_db = PurchaseItemsModel.query.all()

    yield {'purchase_order': po.as_dict(), 'items': [items_from_db[0].as_dict(), items_from_db[1].as_dict()]}

    db.session.query(PurchaseItemsModel).delete()
    db.session.query(PurchaseOrderModel).delete()

    db.session.commit()
