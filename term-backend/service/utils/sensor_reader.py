from datetime import UTC, datetime
from uuid import UUID

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

from service.models.sensors import SensorConfig, SensorData
from service.settings import Settings


class SensorReader:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._bucket = self._settings.INFLUXDB_SENSORS_BUCKET

    async def initialize(self) -> None:
        self.client = InfluxDBClientAsync(
            url=self._settings.INFLUXDB_URL,
            token=self._settings.INFLUXDB_TOKEN,
            org=self._settings.INFLUXDB_ORG,
        )
        self.query_api = self.client.query_api()

    async def get_sensors(self, construction_section_id: UUID) -> list[SensorConfig]:
        query = (
            f'from(bucket: "{self._bucket}") |> range(start: -1d) '
            f'|> filter(fn: (r) => r["construction_section_id"] == "{construction_section_id}") '
            '|> keep(columns: ["sensor_id", "sensor_address", "sensor_name", "sensor_description", '
            '"sensor_unit", "monitoring_name", "monitoring_location", "connection_name", "construction_section_id"]) '
            '|> unique(column: "sensor_id")'
        )
        result = await self.query_api.query(query)
        sensors = []
        for table in result:
            for record in table.records:
                sensors.append(
                    SensorConfig(
                        sensor_id=record["sensor_id"],
                        sensor_address=record["sensor_address"],
                        sensor_name=record["sensor_name"],
                        sensor_description=record["sensor_description"],
                        sensor_unit=record["sensor_unit"],
                        monitoring_name=record["monitoring_name"],
                        monitoring_location=record["monitoring_location"],
                        connection_name=record["connection_name"],
                        construction_section_id=record["construction_section_id"],
                    )
                )
        return sensors

    async def get_sensor_data(
        self, construction_section_id: UUID, sensor_id: str, start: datetime, end: datetime
    ) -> list[SensorData]:
        start_iso = start.replace(tzinfo=UTC).isoformat()
        end_iso = end.replace(tzinfo=UTC).isoformat()

        query = (
            f'from(bucket: "{self._bucket}") |> range(start: {start_iso}, stop: {end_iso}) '
            f'|> filter(fn: (r) => r["construction_section_id"] == "{construction_section_id}" '
            f'and r["sensor_id"] == "{sensor_id}") '
            '|> keep(columns: ["_time", "_value", "monitoring_name", "monitoring_location", "connection_name", '
            '"sensor_address", "sensor_name", "sensor_unit", "sensor_description"]) '
            '|> rename(columns: {"_time": "time", "_value": "value"})'
        )
        result = await self.query_api.query(query)
        sensor_data = []
        for table in result:
            for record in table.records:
                sensor_data.append(
                    SensorData(
                        time=record["time"],
                        value=record["value"],
                        monitoring_name=record["monitoring_name"],
                        monitoring_location=record["monitoring_location"],
                        connection_name=record["connection_name"],
                        sensor_address=record["sensor_address"],
                        sensor_name=record["sensor_name"],
                        sensor_unit=record["sensor_unit"],
                        sensor_description=record["sensor_description"],
                    )
                )
        return sensor_data
