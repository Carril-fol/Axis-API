from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, scoped_session, sessionmaker

from ..config.settings import Config


load_dotenv()


class Base(DeclarativeBase):
    pass

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Database:
    _engine: Engine = None
    _session_factory: sessionmaker = None
    _scoped_session: scoped_session = None

    @classmethod
    def initialize(cls):
        if cls._engine is not None:
            return

        cls._engine = create_engine(
            Config.NEON_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
            future=True,
        )
        cls._session_factory = sessionmaker(
            bind=cls._engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
            class_=Session,
        )
        cls._scoped_session = scoped_session(cls._session_factory)

    @classmethod
    def session(cls) -> Session:
        if cls._scoped_session is None:
            raise RuntimeError("Database is not initialized. Call 'Database.initialize()' first.")

        return cls._scoped_session()

    @classmethod
    def commit(cls) -> None:
        if cls._has_open_session():
            cls._scoped_session.commit()

    @classmethod
    def rollback(cls) -> None:
        if cls._has_open_session():
            cls._scoped_session.rollback()

    @classmethod
    def remove(cls) -> None:
        if cls._scoped_session is not None:
            cls._scoped_session.remove()

    @classmethod
    @contextmanager
    def transaction(cls):
        try:
            yield cls.session()
            cls.commit()
        except Exception:
            cls.rollback()
            raise
        finally:
            cls.remove()

    @classmethod
    def _has_open_session(cls) -> bool:
        return cls._scoped_session is not None and cls._scoped_session.registry.has()
