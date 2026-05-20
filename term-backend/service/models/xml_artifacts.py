import re
from typing import Any

from fastapi_restful.api_model import APIModel
from pydantic import BaseModel, ConfigDict, Field, model_validator
from pydantic.alias_generators import to_pascal


class XmlModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True, alias_generator=to_pascal)


class AddressXml(XmlModel):
    country: str | None = Field(default=None)
    region: str | None = Field(default=None)
    district: str | None = Field(default=None)
    city: str | None = Field(default=None)
    settlement: str | None = Field(default=None)
    street: str | None = Field(default=None)
    building: str | None = Field(default=None)
    room: str | None = Field(default=None)
    note: str | None = Field(default=None)


class IndicatorXml(XmlModel):
    name: str
    value: str
    measure: str


class ConstructionSectionXml(APIModel):
    name: str = Field()
    description: str | None = Field(default=None)
    bim_artifacts: list = Field(default_factory=list)
    has_sensor: bool = Field(default=False)


class ConstructionPartXml(XmlModel):
    object_id: str | None = Field(None, alias="@ObjectID")
    name: str | None = Field(default=None)
    address: AddressXml | None = Field(default=None)

    power_indicators: list[IndicatorXml] = Field(alias="PowerIndicator", default_factory=list)
    technical_indicators: list[IndicatorXml] = Field(alias="TEI", default_factory=list)
    energy_efficiency: str | None = Field(default=None)

    fire_danger_category: str | None = Field(default=None)
    people_permanent_stay: str | None = Field(default=None)
    responsibility_level: str | None = Field(default=None)

    sections: list[ConstructionSectionXml] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def prepare_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        data["PeoplePermanentStay"] = "".join(data.get("PeoplePermanentStay", {}).get("Text", []))
        data["EnergyEfficiency"] = data.get("EnergyEfficiency", {}).get("EnergyEfficiencyClass")
        data["Address"] = data.get("Address", [])[0] if data.get("Address") else None
        return data


class TextBlockXml(XmlModel):
    title: str | None = Field(default=None, alias="@Title")
    text: str | None = Field(default=None, alias="Text")

    @model_validator(mode="before")
    @classmethod
    def prepare_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        text = data.get("Text", [])
        valid_text = " ".join([item.strip() for item in text if item.strip() != "-" and re.search(r"\w+", item)])
        data["Text"] = valid_text or None
        return data


class LinearObjectExtraXml(XmlModel):
    object_category: TextBlockXml | None = Field(default=None, alias="LinearObjectCategory")
    object_class: TextBlockXml | None = Field(default=None, alias="LinearObjectClass")
    object_note: TextBlockXml | None = Field(default=None, alias="LinearObjectNote")
