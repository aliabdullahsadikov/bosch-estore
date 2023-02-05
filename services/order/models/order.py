import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, Integer, Float, String, DateTime, Boolean, Text
from sqlalchemy.orm import relationship

from common.database import Base

ORDER_STATUS = {
    "checkout": 0,
    "shipping": 1,
    "paid": 2,
    "canceled": -1,
    "unprocessed": -2,
    "delivered": 3
}


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    cart_id = Column(String)
    status = Column(Integer, default=0)
    promo_code = Column(String, default=None)
    promo_id = Column(Integer)
    sub_total = Column(Float)
    total_price = Column(Float)

    shipping_type = Column(Integer)
    shipping_comment = Column(Text, nullable=True)
    fio = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    company = Column(String, nullable=True)
    email = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    payment = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    items = relationship("OrderItem")


    # def get_sub_total(self):
    #
