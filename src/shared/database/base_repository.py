from typing import Generic, TypeVar, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import Database


T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    @property
    def db(self) -> Session:
        return Database.session()

    def create(self, entity: T) -> T:
        self.db.add(entity)
        self.db.flush()
        return entity

    def update(self, entity: T) -> T:
        self.db.flush()
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.flush()

    def get_by_id(self, id: int) -> T | None:
        return self.db.get(self.model, id)

    def get_all(self) -> list[T]:
        return self.db.execute(select(self.model)).scalars().all()
