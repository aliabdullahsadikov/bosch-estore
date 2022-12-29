import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, Table
from sqlalchemy.orm import relationship

from common.database import Base


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('user_id', ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role_title = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_at = Column(sqlalchemy.DateTime)

    users = relationship("User", secondary="user_roles", back_populates="roles", cascade="all,delete")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles", cascade="all,delete")

#
#
# roles = sqlalchemy.Table(
#     "roles",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("role_title", sqlalchemy.String, nullable=False),
#     sqlalchemy.Column("description", sqlalchemy.String),
#     sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
#
# )

#
# class UserRole(Base):
#     __tablename__ = "user_roles"
#
#     id = Column(Integer, primary_key=True, index=True)
#     user = Column(Integer, ForeignKey("users.id", ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
#     role = Column(Integer, ForeignKey("roles.id", ondelete='CASCADE', onupdate='CASCADE'))
#     active = Column(Boolean, default=True)
#     created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
#     updated_at = Column(sqlalchemy.DateTime)
#
#     user_role = relationship("User", back_populates="user_role")
#     role_user = relationship("Role", back_populates="role_user")
#



# user_roles = sqlalchemy.Table(
#     "user_roles",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("user", ForeignKey("users.id")),
#     sqlalchemy.Column("role", ForeignKey("roles.id")),
#     sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
# )