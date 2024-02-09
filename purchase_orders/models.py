from db import db


class PurchaseOrderModel(db.Model):
    __tablename__ = 'purchase_order'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, description, quantity):
        self.description = description
        self.quantity = quantity

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}