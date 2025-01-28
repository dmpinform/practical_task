from typing import List

import entities
import settings
from entities import Sensor

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.database_url)

Session = sessionmaker(bind=engine, expire_on_commit=False)


def add_sensors():
    with Session.begin() as session:
        sensor1 = entities.OxygenSensor(
            name='Oxygen Sensor 1',
            oxygen_level=1,
            is_active=True,
        )
        sensor2 = entities.CarbonDioxideSensor(
            name='CO2 Sensor 1',
            co2_level=2,
            is_active=True,
        )
        sensor3 = entities.MoistureSensor(
            name='Moisture Sensor 1',
            moisture_level=3,
            is_active=False,
        )
        sensor4 = entities.SensorOne(
            one_level=111,
        )
        sensor5 = entities.SensorTwo(
            two_level=222,
        )

        session.add(sensor1)
        session.add(sensor2)
        session.add(sensor3)
        session.add(sensor4)
        session.add(sensor5)

        session.commit()


def select_sensors() -> List[Sensor]:
    with Session.begin() as session:
        return session.scalars(select(entities.CarbonDioxideSensor)).all()


def select_one_sensors() -> List[entities.UnionSensors]:
    with Session.begin() as session:
        return session.scalars(select(entities.SensorOne)).all()


def select_two_sensors() -> List[entities.UnionSensors]:
    with Session.begin() as session:
        return session.scalars(select(entities.SensorTwo)).all()


def update_sensor(sensor_id, new_name):
    with Session.begin() as session:
        sensor = session.execute(select(
            Sensor,
        ).filter(
            Sensor.id == sensor_id,
        )).first()

        if sensor:
            sensor.name = new_name
            session.commit()    # Сохраняем изменения
            print(f'Датчик с ID {sensor_id} обновлен. Новое имя: {new_name}')
        else:
            print(f'Датчик с ID {sensor_id} не найден.')


if __name__ == '__main__':
    add_sensors()
    # update_sensor(sensor_id=1, new_name='Updated Oxygen Sensor 1')
    print(select_sensors())
    print(select_one_sensors())
    print(select_two_sensors())
