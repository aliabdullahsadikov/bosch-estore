import sqlalchemy
import datetime

from sqlalchemy import ForeignKey

from common.database import Base
#
# transactions = sqlalchemy.Table(
#     "transactions",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("user_id", ForeignKey("users.id"), index=True),
#     sqlalchemy.Column("transaction_id", sqlalchemy.String, default=None),
#     sqlalchemy.Column("order_id", ForeignKey("orders.id"), index=True),
#     sqlalchemy.Column("status", sqlalchemy.Integer, default=0),
#     sqlalchemy.Column("payment_code", sqlalchemy.String, default=None),
#     sqlalchemy.Column("order_data", sqlalchemy.JSON, default={}),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime)
#
# )
#
