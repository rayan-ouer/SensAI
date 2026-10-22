from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def create_session_factory(database_url: str) -> tuple[Engine, sessionmaker]:
    engine = create_engine(database_url)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)


def get_db_session() -> Session:
    return create_session_factory()
