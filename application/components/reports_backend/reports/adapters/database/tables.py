from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table

SCHEMA_APP = 'app'

naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}

metadata_app = MetaData(naming_convention=naming_convention, schema=SCHEMA_APP)

reports = Table(
    'reports',
    metadata_app,
    Column('id', Integer, primary_key=True),
    Column('name', String(length=50), nullable=False),
    Column('start_at', DateTime, nullable=True),
    Column('end_et', DateTime, nullable=True),
)
