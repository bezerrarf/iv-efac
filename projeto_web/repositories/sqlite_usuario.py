"""Implementação concreta do repositório de usuários em SQLite (LSP)."""

from typing import Optional
from sqlmodel import Session, select
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioRepositoryProtocol
from projeto_web.repositories.database import get_session


class SQLiteUsuarioRepository(UsuarioRepositoryProtocol):
    """Repositório de usuários utilizando SQLite/SQLModel."""

    def __init__(self, session_factory=get_session):
        self._session_factory = session_factory

    def save(self, usuario: Usuario) -> Usuario:
        with self._session_factory() as session:
            if usuario.id is None:
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            else:
                merged = session.merge(usuario)
                session.commit()
                session.refresh(merged)
                return merged

    def find_by_email(self, email: str) -> Optional[Usuario]:
        email_clean = email.strip().lower()
        with self._session_factory() as session:
            statement = select(Usuario).where(Usuario.email == email_clean)
            return session.exec(statement).first()

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        with self._session_factory() as session:
            return session.get(Usuario, user_id)

    def count(self) -> int:
        with self._session_factory() as session:
            statement = select(Usuario)
            return len(session.exec(statement).all())

    def list_all(self) -> list[Usuario]:
        with self._session_factory() as session:
            statement = select(Usuario)
            return list(session.exec(statement).all())
