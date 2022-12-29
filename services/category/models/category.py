from contextlib import contextmanager

import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship, backref

from common.database import Base, SessionLocal


class Category_Product(Base):
    __tablename__ = "category_product"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(ForeignKey('categories.id', onupdate="CASCADE", ondelete="CASCADE"))
    product_id = Column(ForeignKey('products.id', onupdate="CASCADE", ondelete="CASCADE"))



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    parent_id = Column(Integer, default=0)
    slug = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    photo_sm = Column(String, default="default_category_photo_sm.jpg")
    photo_md = Column(String, default="default_category_photo_md.jpg")
    created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_at = Column(sqlalchemy.DateTime)

    products = relationship("Product", secondary="category_product", back_populates="categories", cascade="all,delete")
    children = []
    # children = relationship("Category", backref=backref("parent", remote_side=[id]))

    def __call__(self):
        with get_db() as db:
            child_categories = db.query(Category)\
                .filter(Category.parent_id == self.id, Category.active)\
                .all()
        for child in child_categories:
            child()
        self.children = child_categories


@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
