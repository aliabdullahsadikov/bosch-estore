import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, Integer, Float, Boolean, DateTime

from common.database import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey("orders.id"))
    product_id = Column(ForeignKey("products.id"))
    amount = Column(Integer)
    price = Column(Float)
    sale = Column(Integer, nullable=True)
    sale_percent = Column(Integer, default=0)
    sale_price = Column(Float, default=0.0)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime)

