import uuid
from uuid import UUID

from fastapi_restful.api_model import APIModel
from pydantic import Field

from service.models.s3_artifacts import FileInfo


class TextBlock(APIModel):
    title: str | None = Field(default=None, description="Заголовок сведений")
    text: str | None = Field(default=None, description="Описание")


class LinearObjectExtra(APIModel):
    object_category: TextBlock | None = Field(default=None, description="Сведения о категории линейного объекта")
    object_class: TextBlock | None = Field(default=None, description="Сведения о классе линейного объекта")
    object_note: TextBlock | None = Field(default=None, description="Сведения о линейном объекте")


class Address(APIModel):
    country: str | None = Field(
        default=None,
        description="Страна",
        examples=["Российская Федерация"],
    )
    region: str | None = Field(
        default=None,
        description="Код субъекта Российской Федерации",
        examples=["47"],
    )
    district: str | None = Field(
        default=None,
        description="Наименование района",
        examples=["Всеволожский муниципальный район"],
    )
    city: str | None = Field(
        default=None,
        description="Город",
        examples=["д. Новое Девяткино"],
    )
    settlement: str | None = Field(
        default=None,
        description="Населенный пункт",
        examples=["Новодевяткинское сельское поселение"],
    )
    street: str | None = Field(default=None, description="Улица", examples=["Пушкина"])
    building: str | None = Field(default=None, description="Номер здания/сооружения", examples=["123"])
    room: str | None = Field(default=None, description="Номер помещения", examples=["45"])
    note: str | None = Field(default=None, description="Неформализованное описание адреса")


class Unit(APIModel):
    name: str = Field(description="Наименование единицы измерения", examples=["Миллиметр"])
    symbol: str = Field(description="Символьное обозначение единицы измерения", examples=["мм"])


class Indicator(APIModel):
    name: str = Field(description="Наименование показателя", examples=["Площадь застройки, м2"])
    value: str = Field(description="Значение показателя", examples=["6340,38"])
    measure: str | Unit = Field(description="Единица измерения показателя")


class ConstructionSectionBase(APIModel):
    name: str = Field(description="Название раздела строительства", examples=["Отопление"])
    description: str | None = Field(
        default=None,
        description="Описание раздела строительства",
        examples=["Описание отдела отопление"],
    )
    has_sensor: bool = Field(default=False, description="Признак наличий датчиков", examples=[False])


class ConstructionSectionCreate(ConstructionSectionBase):
    pass


class ConstructionSectionRead(ConstructionSectionBase):
    id: UUID = Field(
        description="Уникальный идентификатор разделов строительства",
    )
    bim_artifacts: list[FileInfo] = Field(
        default_factory=list,
        description="Список BIM-моделй, связанных с разделом строительства",
    )


class ConstructionSectionUpdate(APIModel):
    name: str | None = Field(default=None, description="Название раздела строительства")
    description: str | None = Field(default=None, description="Описание раздела строительства")
    has_sensor: bool | None = Field(default=None, description="Признак наличий датчиков")


class ConstructionPartBase(APIModel):
    object_id: str | None = Field(
        default=None,
        description="Идентификатора объекта (части объекта)",
        examples=["OBJ_28"],
    )
    name: str = Field(
        description="Наименование объекта капитального строительства, входящего в состав сложного объекта",
        examples=["Котельная"],
    )
    address: Address = Field(
        description="Почтовый (строительный) адрес (местоположение) объекта капитального строительства"
    )
    power_indicators: list[Indicator] = Field(
        default_factory=list,
        description="Данные о проектной мощности части объекта",
    )
    technical_indicators: list[Indicator] = Field(
        default_factory=list,
        description="Технико-экономические показатели части объекта",
    )
    energy_efficiency: str | None = Field(
        default=None,
        description="Сведения о классе энергетической эффективности и о повышении энергетической эффективности",
        examples=["A"],
    )
    fire_danger_category: str | None = Field(
        default=None,
        description="Категория пожарной и взрывопожарной опасности",
        examples=["Б"],
    )
    people_permanent_stay: str | None = Field(
        default=None,
        description="Сведения о наличии помещений с постоянным пребыванием людей",
        examples=["Помещения с постоянным пребыванием людей отсутсвуют."],
    )
    responsibility_level: str | None = Field(
        default=None,
        description="Уровень ответственности",
        examples=["нормальный"],
    )


class ConstructionPartCreate(ConstructionPartBase):
    pass


class ConstructionPartRead(ConstructionPartBase):
    id: UUID = Field(default_factory=uuid.uuid4, description="Уникальный строительно объекта")
    sections: list[ConstructionSectionRead] = Field(
        default_factory=list,
        description="Список разделов строительства, связанных с данной частью объекта",
    )


class ConstructionPartUpdate(APIModel):
    object_id: str | None = Field(
        default=None,
        description="Идентификатора объекта (части объекта)",
        examples=["OBJ_28"],
    )
    name: str | None = Field(
        default=None,
        description="Наименование объекта капитального строительства, входящего в состав сложного объекта",
        examples=["Котельная"],
    )
    address: Address | None = Field(
        default=None,
        description="Почтовый (строительный) адрес (местоположение) объекта капитального строительства",
    )
    power_indicators: list[Indicator] | None = Field(
        default=None,
        description="Данные о проектной мощности части объекта",
    )
    technical_indicators: list[Indicator] | None = Field(
        default=None,
        description="Технико-экономические показатели части объекта",
    )
    energy_efficiency: str | None = Field(
        default=None,
        description="Сведения о классе энергетической эффективности и о повышении энергетической эффективности",
        examples=["A"],
    )
    fire_danger_category: str | None = Field(
        default=None,
        description="Категория пожарной и взрывопожарной опасности",
        examples=["Б"],
    )
    people_permanent_stay: str | None = Field(
        default=None,
        description="Сведения о наличии помещений с постоянным пребыванием людей",
        examples=["Помещения с постоянным пребыванием людей отсутсвуют."],
    )
    responsibility_level: str | None = Field(
        default=None,
        description="Уровень ответственности",
        examples=["нормальный"],
    )


class BuildingInfoBase(APIModel):
    name: str | None = Field(
        default=None,
        description="Наименование объекта капитального строительства",
    )
    construction_type: int | None = Field(
        default=None,
        description="Вид работ, на который разрабатывается проектная документация",
    )
    construction_duration: float | None = Field(
        default=None,
        description="Продолжительность работ, месяц",
    )
    address: Address | None = Field(
        default=None,
        description="Почтовый (строительный) адрес (местоположение) объекта капитального строительства",
    )
    technical_indicators: list[Indicator] = Field(
        default_factory=list,
        description="Технико-экономические показатели проектируемого объекта капитального строительства",
    )
    power_indicators: list[Indicator] = Field(
        default_factory=list,
        description="Данные о проектной мощности объекта",
    )
    extra: LinearObjectExtra | None = Field(
        default=None,
        description="Дополнительные сведения спецефичные для линейных объектов",
    )


class BuildingInfoCreate(BuildingInfoBase):
    pass


class BuildingInfoRead(BuildingInfoBase):
    id: UUID = Field(default_factory=uuid.uuid4, description="Уникальный идентификатор здания")
    construction_parts: list[ConstructionPartRead] = Field(
        default_factory=list,
        description="Часть объекта",
    )
    document_artifacts: list[FileInfo] = Field(
        default_factory=list,
        description="Список документов, связанных с разделом строительства",
    )


class BuildingInfoUpdate(APIModel):
    name: str | None = Field(
        default=None,
        description="Наименование объекта капитального строительства",
    )
    construction_type: int | None = Field(
        default=None,
        description="Вид работ, на который разрабатывается проектная документация",
    )
    construction_duration: float | None = Field(
        default=None,
        description="Продолжительность работ, месяц",
    )
    address: Address | None = Field(
        default=None,
        description="Почтовый (строительный) адрес (местоположение) объекта капитального строительства",
    )
    technical_indicators: list[Indicator] | None = Field(
        default=None,
        description="Технико-экономические показатели проектируемого объекта капитального строительства",
    )
    power_indicators: list[Indicator] | None = Field(
        default=None,
        description="Данные о проектной мощности объекта",
    )
    extra: LinearObjectExtra | None = Field(
        default=None,
        description="Дополнительные сведения спецефичные для линейных объектов",
    )
