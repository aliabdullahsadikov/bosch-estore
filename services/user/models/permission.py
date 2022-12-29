import sqlalchemy
import datetime

from sqlalchemy import ForeignKey, Column, Integer, String, Boolean, Table
from sqlalchemy.orm import relationship

from common.database import Base


role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', ForeignKey('roles.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
    Column('permission_id', ForeignKey('permissions.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True)
)


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    permission_title = Column(String, nullable=False)
    description = Column(String)
    active = Column(Boolean, default=True)
    created_at = Column(sqlalchemy.DateTime, default=datetime.datetime.now())
    updated_at = Column(sqlalchemy.DateTime)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions", cascade="all,delete")


# permissions = sqlalchemy.Table(
#     "permissions",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("permission_title", sqlalchemy.String, nullable=False),
#     sqlalchemy.Column("description", sqlalchemy.String),
#     sqlalchemy.Column("active", sqlalchemy.Boolean, default=True),
#     sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=datetime.datetime.now()),
#     sqlalchemy.Column("updated_at", sqlalchemy.DateTime),
#
# )


#
# user_roles = sqlalchemy.Table(
#     "role_permissions",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("role_id", ForeignKey("users.id")),
#     sqlalchemy.Column("permission_id", ForeignKey("roles.id"))
# )