from datetime import datetime
from typing import Dict, Optional, Tuple

import constants

import sqlalchemy.types as types
from sqlalchemy import ForeignKey, Integer, event
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    attribute_keyed_dict,
    attributes,
    keyfunc_mapping,
    mapped_column,
    relationship,
)


class GetValues:

    def get_float(self) -> float:
        ...


class Base(DeclarativeBase):
    pass


# пример пользовательского типа, как альтернатива enum
class StringEnum(types.TypeDecorator):

    impl = types.String(32)

    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enum_type = enum_type

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return self._enum_type(value) if value is not None else None


class SensorStatusType(StringEnum):
    cache_ok = True

    def __init__(self, *args, **kwargs):
        super().__init__(constants.SensorStatusType, *args, **kwargs)


class SensorReadings(Base):
    __tablename__ = 'sensor_readings'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    read_at: Mapped[datetime]
    value: Mapped[Optional[float]]
    status: Mapped[constants.SensorStatusType]
    id_sensor: Mapped[int] = mapped_column(ForeignKey("sensors.id"))
    sensor: Mapped["Sensor"] = relationship(back_populates='readings')

    @property
    def read_key(self) -> Tuple[datetime, SensorStatusType]:
        return self.read_at, self.status


class Sensor(Base):
    __tablename__ = 'sensors'
    TimeLineReadings = (
        Mapped[Dict[Tuple[datetime, SensorStatusType], "SensorReadings"]]
    )
    name: Mapped[str]
    type: Mapped[str]
    is_active: Mapped[bool] = mapped_column(insert_default=False)
    id = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    # Маппинг на словарь для быстрого поиска по дате и статусу
    # Стратегия attribute_keyed_dict
    readings: TimeLineReadings = relationship(
        collection_class=attribute_keyed_dict("read_key"),
        overlaps='readings_id',
        back_populates='sensor',
    )
    # Маппинг на словарь для быстрого поиска ID показания
    # Стратегия keyfunc_mapping
    readings_id: Mapped[Dict[int, "SensorReadings"]] = relationship(
        collection_class=keyfunc_mapping(
            lambda prop: prop.id,
        ),
    # overlaps - устранить предупреждение, что возможны конфликты с readings
    # приложение само должно гаранитировать, что конфликтов не будет
        viewonly=True,
        overlaps='readings'
    )

    __mapper_args__ = {
        'polymorphic_abstract': True,
        'polymorphic_on': 'type',
    }


class OxygenSensor(Sensor):
    __tablename__ = 'oxygen_sensors'

    oxygen_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        primary_key=True,
    )
    __mapper_args__ = {
        'polymorphic_identity': 'oxygen',
    }


class CarbonDioxideSensor(Sensor, GetValues):
    __tablename__ = 'carbon_dioxide_sensors'

    co2_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        primary_key=True,
    )
    __mapper_args__ = {
        'polymorphic_identity': 'carbon',
    }

    def get_float(self) -> float:
        return self.co2_level


class MoistureSensor(Sensor, GetValues):
    __tablename__ = 'moisture_sensors'

    moisture_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"),
        primary_key=True,
    )
    __mapper_args__ = {
        'polymorphic_identity': 'moisture',
    }

    def get_float(self) -> float:
        return self.moisture_level


class UnionSensors(Base):
    __tablename__ = 'union_sensors'

    type: Mapped[str]
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'union',
    }


class SensorOne(UnionSensors):
    one_level: Mapped[Optional[float]]
    __mapper_args__ = {
        'polymorphic_identity': 'one',
    }


class SensorTwo(UnionSensors):
    two_level: Mapped[Optional[float]]
    __mapper_args__ = {
        'polymorphic_identity': 'two',
    }


# Для поддержки согласованности объектов
# @event.listens_for(SensorReadings.read_key, "set")
# def set_item(obj, value, previous, initiator):
#     if obj.sensor is not None:
#         previous = None if previous == attributes.NO_VALUE else previous
#         obj.sensor.readings[value] = obj
#         obj.sensor.readings.pop(previous)
