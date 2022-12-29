import sqlalchemy
import datetime

from sqlalchemy import ForeignKey

from common.database import Base
#
# orders = sqlalchemy.Table(
#     "orders",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("user_id", ForeignKey("users.id"), index=True),
#     sqlalchemy.Column("cart_id", sqlalchemy.Integer),
#     sqlalchemy.Column("status", sqlalchemy.Integer),
#     sqlalchemy.Column("sale_percent", sqlalchemy.Integer, default=0),
#     sqlalchemy.Column("sale_price", sqlalchemy.Float, default=0.0),
#     sqlalchemy.Column("promo_code", sqlalchemy.String, default=None),
#     sqlalchemy.Column("sub_total", sqlalchemy.Float),
#     sqlalchemy.Column("total_price", sqlalchemy.Float),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime)
#
# )

