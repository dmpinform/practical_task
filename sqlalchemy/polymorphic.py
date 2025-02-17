from datetime import datetime, timedelta
from random import random
from typing import List

import declarative
import settings
from constants import SensorStatusType
from declarative import Sensor

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)

Session = sessionmaker(bind=engine, expire_on_commit=False)


def add_sensors():
    with Session.begin() as session:
        sensor1 = declarative.OxygenSensor(
            name='Oxygen Sensor 1',
            oxygen_level=1,
            is_active=True,
        )

        sensor2 = declarative.CarbonDioxideSensor(
            name='CO2 Sensor 1',
            co2_level=2,
            is_active=True,
        )
        sensor3 = declarative.MoistureSensor(
            name='Moisture Sensor 1',
            moisture_level=3,
            is_active=False,
        )
        sensor4 = declarative.SensorOne(
            one_level=111,
        )
        sensor5 = declarative.SensorTwo(
            two_level=222,
        )

        session.add(sensor1)
        session.add(sensor2)
        session.add(sensor3)
        session.add(sensor4)
        session.add(sensor5)

        session.commit()


def select_sensors():
    with Session.begin() as session:
        return session.execute(select(declarative.Sensor))


def select_one_sensors() -> List[declarative.UnionSensors]:
    with Session.begin() as session:
        return session.scalars(select(declarative.SensorOne)).all()


def select_two_sensors() -> List[declarative.UnionSensors]:
    with Session.begin() as session:
        return session.scalars(select(declarative.SensorTwo)).all()


def add_sensor_readings():
    with Session.begin() as session:
        sensors = session.scalars(select(Sensor))
        reade_at = datetime(2024, 2, 2)
        for num, sensor in enumerate(sensors):
            reade_at += timedelta(hours=num)

            sensor.readings.setdefault(
                (reade_at, SensorStatusType.GOOD),
                declarative.SensorReadings(
                    read_at=reade_at,
                    value=random(),
                    status=SensorStatusType.GOOD.value,
                ),
            )
            sensor.readings.setdefault(
                (reade_at, SensorStatusType.ERROR),
                declarative.SensorReadings(
                    read_at=reade_at,
                    value=random(),
                    status=SensorStatusType.ERROR.value,
                ),
            )


def add_back_mutation():
    reade_at = datetime(2030, 2, 2)
    new_reade_at = datetime(2055, 2, 2)
    sensor = declarative.OxygenSensor(
        name='Oxygen Sensor test',
        oxygen_level=1,
        is_active=True,
    )
    reading = declarative.SensorReadings(
        read_at=reade_at,
        value=random(),
        status=SensorStatusType.ERROR.value,
        sensor=sensor,
    )
    reading.read_at = new_reade_at
    # ключ в коллекции словарей не изменится и будет равен reade_at
    print(sensor.readings.items())
    # вставка в бд корректна
    with Session.begin() as session:
        session.add(sensor)


def initial_rows():
    add_sensors()
    add_sensor_readings()


if __name__ == '__main__':

    # запрос датчиков и выбор значений показаний
    # по ключу: дата показания + статус
    # по ключу: идентификатор показания

    check_date = datetime(2024, 2, 11, 15)
    check_error = (check_date, SensorStatusType.ERROR)
    find_reading_id = 607
    with Session.begin() as session:
        query = session.scalars(select(declarative.Sensor))

        for sensor in query:
            reading_error = sensor.readings.get(check_error)
            find_reading = sensor.readings_id.get(find_reading_id)

            if reading_error:
                print('error_value', reading_error.value)

            if find_reading:
                print('reading', find_reading.value)

    # запрос разных датчиков из одной таблицы
    print(select_one_sensors())
    print(select_two_sensors())
