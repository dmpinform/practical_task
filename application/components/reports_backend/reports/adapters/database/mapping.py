from reports.application import entities
from sqlalchemy.orm import registry

from . import tables

mapper = registry()

mapper.map_imperatively(entities.Reports, tables.reports)
