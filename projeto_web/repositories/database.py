"""Configuração da engine do banco de dados SQLite e sessões."""

from sqlmodel import Session, SQLModel, create_engine
from projeto_web.core.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


def init_db():
    """Cria tabelas e habilita o modo WAL no SQLite."""
    SQLModel.metadata.create_all(engine)
    if "sqlite" in DATABASE_URL:
        with engine.connect() as conn:
            conn.exec_driver_sql("PRAGMA journal_mode=WAL;")
            conn.exec_driver_sql("PRAGMA synchronous=NORMAL;")


def get_session() -> Session:
    """Retorna uma nova sessão do banco de dados."""
    return Session(engine)
