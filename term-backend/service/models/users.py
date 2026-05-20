from __future__ import annotations

import uuid
from enum import StrEnum, auto
from uuid import UUID

from fastapi_restful.api_model import APIModel
from fastapi_users.schemas import BaseUser, BaseUserCreate, BaseUserUpdate
from pydantic import Field, field_serializer
from pydantic_extra_types.phone_numbers import PhoneNumber


class АccountRole(StrEnum):
    ENGINEER = auto()
    CHIEF_ENGINEER = auto()


class _BaseGroup(APIModel):
    name: str = Field(description="Имя группы", examples=["Отдел теплоснабжения"])
    description: str = Field(description="Описание группы", examples=["Отдел занимается теплоснабжением"])


class GroupRead(_BaseGroup):
    id: UUID = Field(default_factory=uuid.uuid4, description="Уникальный идентификатор группы")
    users: list[_BaseUser] | None = Field(default=None, description="Список пользователей в группе", examples=[])


class GroupWithoutUserRead(_BaseGroup):
    id: UUID = Field(default_factory=uuid.uuid4, description="Уникальный идентификатор группы")


class GroupCreate(_BaseGroup):
    pass


class GroupUpdate(APIModel):
    name: str | None = Field(default=None, description="Имя группы")
    description: str | None = Field(default=None, description="Описание группы")


class _BaseUser(BaseUser[UUID]):
    is_verified: bool = True
    first_name: str = Field(description="Имя", examples=["Иван"])
    last_name: str = Field(description="Фамиля", examples=["Иванов"])
    middle_name: str | None = Field(default=None, description="Отчестов", examples=["Иванович"])
    mobile_phone: PhoneNumber | None = Field(default=None, description="Номер телефона", examples=["+79991234567"])
    role: АccountRole = Field(
        default=АccountRole.ENGINEER,
        description="Роли пользователя: 'engineer' или 'chief_engineer'",
        examples=[АccountRole.ENGINEER, АccountRole.CHIEF_ENGINEER],
    )


class UserRead(_BaseUser):
    groups: list[GroupWithoutUserRead] | None = Field(
        default=None, description="Список групп в которых состоит пользователь", examples=[]
    )

    @field_serializer("mobile_phone")
    def format_mobile_phone(self, value: PhoneNumber | None) -> str | None:
        if value:
            return str(value).replace("tel:", "")
        return value


class UserCreate(BaseUserCreate):
    role: АccountRole = Field(
        default=АccountRole.ENGINEER,
        description="Роли пользователя: 'engineer' или 'chief_engineer'",
        examples=[АccountRole.ENGINEER, АccountRole.CHIEF_ENGINEER],
    )
    first_name: str = Field(description="Имя", examples=["Иван"])
    last_name: str = Field(description="Фамиля", examples=["Иванов"])
    middle_name: str | None = Field(default=None, description="Отчестов", examples=["Иванович"])
    mobile_phone: PhoneNumber | None = Field(default=None, description="Номер телефона", examples=["+79991234567"])


class UserUpdate(BaseUserUpdate):
    role: АccountRole | None = Field(default=None, description="Роли пользователя: 'engineer' или 'chief_engineer'")
    first_name: str | None = Field(default=None, description="Имя", examples=["Иван"])
    last_name: str | None = Field(default=None, description="Фамиля", examples=["Иванов"])
    middle_name: str | None = Field(default=None, description="Отчестов", examples=["Иванович"])
    mobile_phone: PhoneNumber | None = Field(default=None, description="Номер телефона", examples=["+79991234567"])
