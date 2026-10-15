"""Implementação concreta de comandos de escrita de usuários em SQLite (CQRS - Command Side)."""

from typing import Optional
from sqlmodel import Session
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioCommandRepositoryProtocol
from projeto_web.repositories.database import get_session


class SQLiteUsuarioCommandRepository(UsuarioCommandRepositoryProtocol):
    """Repositório especializado exclusivamente em comandos de escrita e alteração de estado."""

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

    def update_role(self, user_id: int, role: str) -> Optional[Usuario]:
        with self._session_factory() as session:
            usuario = session.get(Usuario, user_id)
            if usuario:
                usuario.role = role
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            return None

    def toggle_presenca(self, user_id: int, dia: Optional[str] = None) -> Optional[Usuario]:
        with self._session_factory() as session:
            usuario = session.get(Usuario, user_id)
            if usuario:
                if dia == "Dia 1":
                    usuario.presenca_dia1 = not bool(usuario.presenca_dia1)
                elif dia == "Dia 2":
                    usuario.presenca_dia2 = not bool(usuario.presenca_dia2)
                else:
                    novo_status = not bool(usuario.presenca_dia1 or usuario.presenca_dia2 or usuario.presenca_confirmada)
                    usuario.presenca_dia1 = novo_status
                    usuario.presenca_dia2 = novo_status

                usuario.presenca_confirmada = bool(usuario.presenca_dia1 or usuario.presenca_dia2)
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            return None

    def update_foto(self, user_id: int, foto_url: str) -> Optional[Usuario]:
        with self._session_factory() as session:
            usuario = session.get(Usuario, user_id)
            if usuario:
                usuario.foto_url = foto_url
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            return None

    def update_senha(self, user_id: int, nova_senha_hash: str) -> Optional[Usuario]:
        with self._session_factory() as session:
            usuario = session.get(Usuario, user_id)
            if usuario:
                usuario.senha_hash = nova_senha_hash
                session.add(usuario)
                session.commit()
                session.refresh(usuario)
                return usuario
            return None
    def delete(self, user_id: int) -> bool:
        with self._session_factory() as session:
            usuario = session.get(Usuario, user_id)
            if usuario:
                session.delete(usuario)
                session.commit()
                return True
            return False

