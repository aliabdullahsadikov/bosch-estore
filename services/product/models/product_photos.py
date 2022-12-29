import sqlalchemy
import uuid
import datetime

from sqlalchemy import ForeignKey, Column, String, Boolean, Integer, Float, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.database import Base


class ProductPhoto(Base):
    __tablename__ = "product_photos"

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey("products.id", ondelete="CASCADE", onupdate="CASCADE"))
    main = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    photo_sm = Column(String, default="default_product_photo_sm.jpg")
    photo_md = Column(String, default="default_product_photo_md.jpg")
    photo_lg = Column(String, default="default_product_photo_lg.jpg")

    product = relationship("Product", back_populates="photos", cascade="all,delete")
