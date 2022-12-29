import sqlalchemy
import datetime

from sqlalchemy import ForeignKey

from common.database import Base
#
# order_items = sqlalchemy.Table(
#     "order_items",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("order_id", ForeignKey("orders.id")),
#     sqlalchemy.Column("product_id", ForeignKey("products.id")),
#     sqlalchemy.Column("amount", sqlalchemy.Integer),
#     sqlalchemy.Column("price", sqlalchemy.Float),
#     sqlalchemy.Column("sale_percent", sqlalchemy.Integer, default=0),
#     sqlalchemy.Column("sale_price", sqlalchemy.Float, default=0.0),
#     sqlalchemy.Column("status", sqlalchemy.Boolean, default=True),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime)
#
# )

