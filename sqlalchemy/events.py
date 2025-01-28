from typing import List

import constants
import entities
import settings
from entities import Sensor

from sqlalchemy import create_engine, event, select, true
from sqlalchemy.orm import ORMExecuteState, sessionmaker, with_loader_criteria

engine = create_engine(settings.database_url)
Session = sessionmaker(bind=engine, expire_on_commit=False)


# Core DialectEvents
@event.listens_for(engine, 'do_connect')
def receive_do_connect(dialect, conn_rec, cargs, cparams):
    print(*cargs, {**cparams})
    cparams['password'] = constants.DB_APP_PASS


# Core ConnectionEvents
@event.listens_for(engine, 'after_execute')
def receive_after_execute(
    conn, clauseelement, multiparams, params, execution_options, result
):
    print(clauseelement)


@event.listens_for(engine, 'before_execute')
def receive_before_execute(
    conn, clauseelement, multiparams, params, execution_options
):
    print(clauseelement)


# ORM SessionEvents
@event.listens_for(Session, 'after_begin')
def receive_after_begin(session, transaction, connection):
    print(connection)


@event.listens_for(Session, 'do_orm_execute')
def receive_do_orm_execute(orm_execute_state):
    # return: ORMExecuteState
    state: ORMExecuteState = orm_execute_state
    print(state.bind_arguments)


@event.listens_for(Session, 'do_orm_execute')
def _add_filtering_criteria(execute_state):
    is_select = execute_state.is_select
    is_column_load = execute_state.is_column_load
    is_relationship_load = execute_state.is_relationship_load

    if (is_select and not is_column_load and not is_relationship_load
            and not execute_state.execution_options.get('view_all', False)):

        execute_state.statement = execute_state.statement.options(
            with_loader_criteria(
                Sensor,
                lambda cls: cls.is_active == true(),
                include_aliases=True,
            )
        )


def select_sensors_carbon() -> List[Sensor]:
    with Session.begin() as session:
        return session.scalars(
            select(
                entities.CarbonDioxideSensor,
            ).execution_options(view_all=False)
        ).all()


def select_sensors_moisture() -> List[Sensor]:
    with Session.begin() as session:
        return session.scalars(
            select(
                entities.MoistureSensor,
            ).execution_options(view_all=False)
        ).all()


def select_all() -> List[Sensor]:
    session = Session()
    all_sensors = session.scalars(
        select(Sensor).execution_options(view_all=True)
    ).all()
    return list(all_sensors)


if __name__ == '__main__':
    sensors: List[entities.Sensor] = select_all()
    print(sensors)
