import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, JSON, DateTime

from common.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), index=True)
    transaction = Column(String, default=None)
    order_id = Column(ForeignKey("orders.id"), index=True)
    payment_code = Column(String, default=None)
    order_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())
    cancel_time = Column(DateTime)
    state = Column(Integer, default=0)
    reason = Column(String, default=None)
