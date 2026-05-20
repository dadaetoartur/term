from datetime import UTC, datetime
from functools import partial
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FileInfo(BaseModel):
    artifacts_id: UUID = Field(
        examples=[str(uuid4())],
        description="Уникальный идентификатор директории, где расположены артефакты",
    )
    filename: str = Field(
        examples=["small.frag", "small.json"],
        description="Имя сохраненного артефакта",
    )
    file_path: str = Field(
        examples=[f"{uuid4()}/small.frag"],
        description="Полный путь до артефакта. Использовать в методах с 'file_path'",  # noqa: RUF001
    )
    last_modified: datetime | None = Field(
        default_factory=partial(datetime.now, tz=UTC),
        examples=[datetime.now(UTC)],
        description="Время сохранения файла",
    )
    model_config = ConfigDict(populate_by_name=True)

    @model_validator(mode="before")
    @classmethod
    def check_card_number_omitted(cls, data: dict[str, Any]) -> Any:
        if key := data.get("Key"):
            artifacts_id, filename = key.split("/")
            data.setdefault("artifacts_id", artifacts_id)
            data.setdefault("filename", filename)
            data.setdefault("file_path", data["Key"])
            data.setdefault("last_modified", data["LastModified"])

        return data
