from dataclasses import dataclass

from sqlalchemy.orm import Session

from .transaction import TransactionContext


@dataclass
class BaseRepository:
    """
    Base class for Repositories, using SQLAlchemy
    """
    context: TransactionContext

    @property
    def session(self) -> Session:
        return self.context.current_session
