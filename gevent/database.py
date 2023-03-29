from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine

metadata = MetaData()

rate_table = Table(
    'rate',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('rate_at', String, nullable=True),
    Column('price', String, nullable=True),
)


def get_engine():
    engine = create_engine('sqlite:///')
    metadata.create_all(engine)
    return engine
