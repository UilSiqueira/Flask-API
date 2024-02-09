from db import db


class PurchaseItemsModel(db.Model):
    __tablename__ = 'purchase_orders_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    purchase_order_id = db.Column(db.Integer, db.ForeignKey(
        'purchase_order.id'), nullable=False)

    def __init__(self, description, price, quantity, purchase_order_id):
        self.description = description
        self.price = price
        self.quantity = quantity
        self.purchase_order_id = purchase_order_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
