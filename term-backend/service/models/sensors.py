from datetime import datetime

from pydantic import BaseModel, Field


class SensorConfig(BaseModel):
    sensor_id: str = Field(description="Идентификатор датчика", examples=["3.Left.1.1"])
    sensor_address: str = Field(description="Адрес датчика", examples=["0x20"])
    sensor_name: str = Field(description="Имя датчика", examples=["Датчик температуры стены"])
    sensor_description: str = Field(
        description="Описание датчика", examples=["Датчик температуры стены, подключен к порту 1"]
    )
    sensor_unit: str = Field(description="Единица измерения датчика", examples=["C"])
    monitoring_name: str = Field(description="Название мониторинга", examples=["Экспериментальный павильон"])
    monitoring_location: str = Field(
        description="Местоположение мониторинга", examples=["Локомотивом проезд д.21 стр 4, 55.844711, 37.571941"]
    )
    connection_name: str = Field(description="Название подключения", examples=["YC1001_1"])
    construction_section_id: str = Field(
        description="Уникальный идентификатор разделов строительства", examples=["00000000-0000-0000-0000-000000000000"]
    )


class SensorData(BaseModel):
    time: datetime = Field(description="Время записи данных", examples=["2024-06-27T17:38:32.832784Z"])
    value: float = Field(description="Значение датчика", examples=[19.03])
    monitoring_name: str = Field(description="Название мониторинга", examples=["Экспериментальный павильон"])
    monitoring_location: str = Field(
        description="Местоположение мониторинга", examples=["Локомотивом проезд д.21 стр 4, 55.844711, 37.571941"]
    )
    connection_name: str = Field(description="Название подключения", examples=["YC1001_1"])
    sensor_address: str = Field(description="Адрес датчика", examples=["32"])
    sensor_name: str = Field(description="Имя датчика", examples=["Датчик температуры стены"])
    sensor_unit: str = Field(description="Единица измерения датчика", examples=["C"])
    sensor_description: str = Field(
        description="Описание датчика", examples=["Датчик температуры стены, подключен к порту 1"]
    )
