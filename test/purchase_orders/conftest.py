import pytest
from db import db

from purchase_orders.models import PurchaseOrderModel


@pytest.fixture()
def purchase_on_db():
    purchases = [
        PurchaseOrderModel('Purchase Order Teste', 50),
        PurchaseOrderModel('Purchase Order Teste2', 150)
    ]

    for purchase in purchases:
        db.session.add(purchase)

    db.session.commit()

    for purchase in purchases:
        db.session.refresh(purchase)

    yield purchases

    db.session.query(PurchaseOrderModel).delete()

    db.session.commit()
