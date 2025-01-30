import settings
from declarative import Base

from sqlalchemy import create_engine

engine = create_engine(settings.database_url)

Base.metadata.create_all(engine)

print("Таблицы успешно созданы!")
