from urllib.parse import quote

from pydantic import BaseSettings


class SettingsDB(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASS: str

    ALEMBIC_SCRIPT_LOCATION: str = 'reports.adapters.database:alembic'

    ALEMBIC_VERSION_LOCATIONS: str = 'reports.adapters.database:migrations'

    ALEMBIC_MIGRATION_FILENAME_TEMPLATE: str = (
        '%%(year)d_'
        '%%(month).2d_'
        '%%(day).2d_'
        '%%(hour).2d_'
        '%%(minute).2d_'
        '%%(second).2d_'
        '%%(slug)s'
    )

    LOGGING_LEVEL: str = 'INFO'
    SA_LOGS: bool = False

    @property
    def DATABASE_URL(self):
        url = (
            'postgresql+psycopg2://{db_user}:{db_pass}'
            '@{db_host}:{db_port}/{db_name}'
        )

        return url.format(
            db_user=self.DATABASE_USER,
            db_pass=quote(self.DATABASE_PASS),
            db_host=self.DATABASE_HOST,
            db_port=self.DATABASE_PORT,
            db_name=self.DATABASE_NAME,
        )

    @property
    def LOGGING_CONFIG(self):
        config = {
            'loggers': {
                'alembic': {
                    'handlers': ['default'],
                    'level': self.LOGGING_LEVEL,
                    'propagate': False,
                }
            }
        }

        if self.SA_LOGS:
            config['loggers']['sqlalchemy'] = {
                'handlers': ['default'],
                'level': self.LOGGING_LEVEL,
                'propagate': False,
            }

        return config
