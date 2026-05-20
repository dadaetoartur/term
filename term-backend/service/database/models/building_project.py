from __future__ import annotations

import uuid

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Uuid
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from service.database.common import BaseTable


class ConstructionSection(BaseTable):
    __tablename__ = "construction_section"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    bim_artifacts: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)
    has_sensor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    construction_part_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("construction_part.id", ondelete="CASCADE"))
    construction_part: Mapped[ConstructionPart] = relationship(
        "ConstructionPart", back_populates="sections", lazy="joined"
    )


class ConstructionPart(BaseTable):
    __tablename__ = "construction_part"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[dict] = mapped_column(JSONB, nullable=True)
    power_indicators: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)
    technical_indicators: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)
    energy_efficiency: Mapped[str] = mapped_column(String, nullable=True)
    fire_danger_category: Mapped[str] = mapped_column(String, nullable=True)
    people_permanent_stay: Mapped[str] = mapped_column(String, nullable=True)
    responsibility_level: Mapped[str] = mapped_column(String, nullable=True)

    sections: Mapped[list[ConstructionSection]] = relationship(
        "ConstructionSection",
        back_populates="construction_part",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    building_info_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("building_info.id", ondelete="CASCADE"))
    building_info: Mapped[BuildingInfo] = relationship(
        "BuildingInfo",
        back_populates="construction_parts",
        lazy="joined",
    )


class BuildingInfo(BaseTable):
    __tablename__ = "building_info"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    construction_type: Mapped[int] = mapped_column(Integer, nullable=True)
    construction_duration: Mapped[float] = mapped_column(Float, nullable=True)
    address: Mapped[dict] = mapped_column(JSONB, nullable=True)
    technical_indicators: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)
    power_indicators: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)
    extra: Mapped[dict] = mapped_column(JSONB, default={}, nullable=True)
    document_artifacts: Mapped[list[dict]] = mapped_column(JSONB, default=[], nullable=True)

    construction_parts: Mapped[list[ConstructionPart]] = relationship(
        "ConstructionPart",
        back_populates="building_info",
        cascade="all, delete-orphan",
        lazy="joined",
    )
