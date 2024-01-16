from reports.adapters.database import settings, transaction
from sqlalchemy import create_engine

context_db_app = transaction.TransactionContext(
    bind=create_engine(settings.SettingsDB().DATABASE_URL),
)
