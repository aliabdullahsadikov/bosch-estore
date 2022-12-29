import sqlalchemy
import uuid
import datetime

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from common.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    firstname = Column(String, nullable=False)
    lastname = Column(String)
    password_hash = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    phone_verified = Column(Boolean, default=False)
    otp_secret = Column(String, default=None)
    status = Column(Integer, default=0)
    email = Column(String, unique=True, index=True)
    created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_at = Column(sqlalchemy.DateTime)

    roles = relationship("Role", secondary="user_roles", back_populates="users", cascade="all,delete")



#
# users = sqlalchemy.Table(
#     "users",
#     metadata,
#     sqlalchemy.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
#     sqlalchemy.Column("firstname", sqlalchemy.String, nullable=False),
#     sqlalchemy.Column("lastname", sqlalchemy.String),
#     sqlalchemy.Column("password_hash", sqlalchemy.String),
#     sqlalchemy.Column("phone", sqlalchemy.Integer, nullable=False),
#     sqlalchemy.Column("phone_verified", sqlalchemy.Boolean, default=False),
#     sqlalchemy.Column("otp_secret", sqlalchemy.String),
#     sqlalchemy.Column("email", sqlalchemy.String),
#     sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
#
# )
