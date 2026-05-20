from pathlib import Path
from typing import Any

import xmlschema
from pydantic import TypeAdapter, ValidationError

from service.constants import CONSTRUCTION_SECTIONS
from service.database.models.building_project import BuildingInfo, ConstructionPart, ConstructionSection
from service.models.xml_artifacts import (
    AddressXml,
    ConstructionPartXml,
    IndicatorXml,
    LinearObjectExtraXml,
)


class XMLSchemaProcessorError(Exception):
    pass


class XMLSchemaProcessor:
    def __init__(self, xsd_path: Path, units_map_path: Path):
        self._xml_schema = xmlschema.XMLSchema(xsd_path)
        self._id_to_unit = TypeAdapter(dict[str, dict[str, Any]]).validate_json(units_map_path.read_text())

        self._list_construction_part = TypeAdapter(list[ConstructionPartXml])
        self._list_indicators = TypeAdapter(list[IndicatorXml])

        self._expected_building_keys = ["IndustrialObject", "NonIndustrialObject", "LinearObject"]

    def process_xml(self, raw_data: bytes) -> BuildingInfo:
        if not self._xml_schema.is_valid(raw_data):
            raise ValueError("Provided XML is not valid according to the XSD.")

        data: dict[str, Any] = self._xml_schema.to_dict(raw_data)  # type: ignore[assignment]

        building_info_data, type_building_info = next(
            (data[key], key) for key in self._expected_building_keys if key in data
        )
        return self._make_building_info(building_info_data, type_building_info)

    def _make_building_info(self, raw_building_info_data: dict[str, Any], type_building_info: str) -> BuildingInfo:
        try:
            technical_indicators = self._prepare_units(
                self._list_indicators.validate_python(raw_building_info_data.get("TEI", []))
            )
            power_indicators = self._prepare_units(
                self._list_indicators.validate_python(raw_building_info_data.get("PowerIndicator", []))
            )

            oks_parts = self._find_oks(raw_building_info_data)
            construction_parts = self._list_construction_part.validate_python(oks_parts)
            orm_construction_parts = []
            for construction_part in construction_parts:
                construction_section = [
                    ConstructionSection(name=section, description=None, bim_artifacts=[])  # type: ignore[call-arg]
                    for section in CONSTRUCTION_SECTIONS
                ]
                orm_construction_part = ConstructionPart(
                    object_id=construction_part.object_id,  # type: ignore[call-arg]
                    name=construction_part.name,
                    address=AddressXml.model_validate(construction_part.address).model_dump(),
                    power_indicators=self._prepare_units(construction_part.power_indicators),
                    technical_indicators=self._prepare_units(construction_part.technical_indicators),
                    energy_efficiency=construction_part.energy_efficiency,
                    fire_danger_category=construction_part.fire_danger_category,
                    people_permanent_stay=construction_part.people_permanent_stay,
                    responsibility_level=construction_part.responsibility_level,
                    sections=construction_section,
                )
                orm_construction_parts.append(orm_construction_part)

            extra = None
            if type_building_info == "LinearObject":
                extra = LinearObjectExtraXml.model_validate(raw_building_info_data)

            return BuildingInfo(
                name=raw_building_info_data.get("Name"),  # type: ignore[call-arg]
                construction_type=raw_building_info_data.get("ConstructionType"),
                construction_duration=raw_building_info_data.get("ConstructionDuration"),
                address=AddressXml.model_validate(raw_building_info_data.get("Address", {})).model_dump(),
                technical_indicators=technical_indicators,
                power_indicators=power_indicators,
                construction_parts=orm_construction_parts,
                extra=extra.model_dump() if extra else None,
            )

        except ValidationError as ve:
            raise XMLSchemaProcessorError(f"Validation error when creating BuildingInfo: {ve}") from None

    def _find_oks(self, data: dict[str, Any], oks_parts: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
        if oks_parts is None:
            oks_parts = []
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "OKS":
                    if isinstance(value, list):
                        oks_parts.extend(value)
                    else:
                        oks_parts.append(value)
                else:
                    self._find_oks(value, oks_parts)
        elif isinstance(data, list):
            for item in data:
                self._find_oks(item, oks_parts)
        return oks_parts

    def _prepare_units(self, items: list[IndicatorXml]) -> list[dict[str, Any]]:
        return [
            {"name": item.name, "value": item.value, "measure": self._id_to_unit.get(item.measure) or item.measure}
            for item in items
        ]
