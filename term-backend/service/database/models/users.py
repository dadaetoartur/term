from __future__ import annotations

import uuid
from enum import StrEnum, auto

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Enum as SqlEnum, ForeignKey, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from service.database.common import BaseTable


class АccountRole(StrEnum):
    ENGINEER = auto()
    CHIEF_ENGINEER = auto()


class UserGroup(BaseTable):
    __tablename__ = "user_group"

    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    group_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("group.id", ondelete="CASCADE"), primary_key=True)

    user: Mapped[User] = relationship("User", back_populates="group_associations", lazy="joined")
    group: Mapped[Group] = relationship("Group", back_populates="user_associations", lazy="joined")


class User(BaseTable, SQLAlchemyBaseUserTableUUID):
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    middle_name: Mapped[str] = mapped_column(String, nullable=True)
    mobile_phone: Mapped[str] = mapped_column(String, nullable=True)
    role: Mapped[АccountRole] = mapped_column(SqlEnum(АccountRole), default=АccountRole.ENGINEER)

    groups: Mapped[list[Group]] = relationship(
        secondary="user_group", lazy="joined", back_populates="users", viewonly=True
    )
    group_associations: Mapped[list[UserGroup]] = relationship("UserGroup", back_populates="user", lazy="joined")


class Group(BaseTable):
    __tablename__ = "group"
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String, unique=True)
    description: Mapped[str] = mapped_column(String)

    users: Mapped[list[User]] = relationship(
        secondary="user_group", lazy="joined", back_populates="groups", viewonly=True
    )
    user_associations: Mapped[list[UserGroup]] = relationship(
        "UserGroup", back_populates="group", lazy="joined", cascade="all, delete-orphan"
    )
