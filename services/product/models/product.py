import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, String, Boolean, Integer, Float, Text
from sqlalchemy.orm import relationship

from common.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    long_name = Column(String)
    model = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    status = Column(Integer, default=1)
    manufacturer = Column(String, default=None)
    amount = Column(Integer)
    description_uz = Column(Text)
    description_ru = Column(Text)
    description_en = Column(Text)
    content_uz = Column(Text)
    content_ru = Column(Text)
    content_en = Column(Text)
    info_uz = Column(Text)
    info_ru = Column(Text)
    info_en = Column(Text)
    views = Column(Integer)
    tags = Column(Text)
    created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_at = Column(sqlalchemy.DateTime)

    categories = relationship("Category", secondary="category_product", back_populates="products", cascade="all,delete")
    photos = relationship("ProductPhoto", back_populates="product", cascade="all,delete")
