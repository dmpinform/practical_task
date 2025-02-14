from datetime import datetime
from typing import Optional

import constants

import sqlalchemy.types as types
from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    MappedAsDataclass,
    mapped_column,
)


class GetValues:

    def get_float(self) -> float:
        ...


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Sensor(Base):
    __tablename__ = 'sensors'

    name: Mapped[str]
    type: Mapped[str] = mapped_column(init=False)
    is_active: Mapped[bool] = mapped_column(insert_default=False)
    id = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    __mapper_args__ = {
        'polymorphic_abstract': True,
        'polymorphic_on': 'type',
    }


class OxygenSensor(Sensor):
    __tablename__ = 'oxygen_sensors'

    oxygen_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"), primary_key=True, init=False
    )
    # readings: Mapped[Optional[List['SensorReadings']]] = relationship(
    #     'SensorReadings', default_factory=list
    # )
    __mapper_args__ = {
        'polymorphic_identity': 'oxygen',
    }



class CarbonDioxideSensor(Sensor, GetValues):
    __tablename__ = 'carbon_dioxide_sensors'

    co2_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"), primary_key=True, init=False
    )
    # readings: Mapped[Optional[List['SensorReadings']]] = relationship(
    #     'SensorReadings', default_factory=list
    # )
    __mapper_args__ = {
        'polymorphic_identity': 'carbon',
    }

    def get_float(self) -> float:
        return self.co2_level


class MoistureSensor(Sensor, GetValues):
    __tablename__ = 'moisture_sensors'

    moisture_level: Mapped[float]
    id: Mapped[int] = mapped_column(
        ForeignKey("sensors.id"), primary_key=True, init=False
    )
    # readings: Mapped[Optional[List['SensorReadings']]] = relationship(
    #     'SensorReadings', default_factory=list
    # )
    __mapper_args__ = {
        'polymorphic_identity': 'moisture',
    }

    def get_float(self) -> float:
        return self.moisture_level


class UnionSensors(Base):
    __tablename__ = 'union_sensors'

    type: Mapped[str] = mapped_column(init=False)
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False
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


class StringEnum(types.TypeDecorator):

    impl = types.String(32)

    def __init__(self, enum_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enum_type = enum_type

    def process_bind_param(self, value, dialect):
        return value.value if value is not None else None

    def process_result_value(self, value, dialect):
        return self._enum_type(value) if value is not None else None


# class SensorStatusType(StringEnum):
#     cache_ok = True
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(constants.SensorStatusType, *args, **kwargs)
#
#
# class SensorReadings(Base):
#     __tablename__ = 'sensor_readings'
#
#     id: Mapped[int] = mapped_column(
#         primary_key=True, autoincrement=True, init=False
#     )
#     read_at: Mapped[datetime]
#     value: Mapped[Optional[float]]
#     status: Mapped[constants.SensorStatusType]
#     id_sensor: Mapped[int] = mapped_column(ForeignKey("sensors.id"), init=False)
