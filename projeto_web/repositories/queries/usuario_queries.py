"""Implementação concreta de consultas e projeções de usuários em SQLite (CQRS - Query Side)."""

from typing import List, Optional
from sqlmodel import Session, select, func
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioQueryRepositoryProtocol
from projeto_web.repositories.database import get_session


class SQLiteUsuarioQueryRepository(UsuarioQueryRepositoryProtocol):
    """Repositório especializado exclusivamente em consultas de leitura e projeções otimizadas."""

    def __init__(self, session_factory=get_session):
        self._session_factory = session_factory

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        with self._session_factory() as session:
            return session.get(Usuario, user_id)

    def find_by_email(self, email: str) -> Optional[Usuario]:
        if not email:
            return None
        email_clean = email.strip().lower()
        with self._session_factory() as session:
            # Busca exata primeiro (usa índice) e fallback case-insensitive/trim para máxima compatibilidade
            statement = select(Usuario).where(Usuario.email == email_clean)
            encontrado = session.exec(statement).first()
            if encontrado is not None:
                return encontrado
            statement_ci = select(Usuario).where(func.lower(func.trim(Usuario.email)) == email_clean)
            return session.exec(statement_ci).first()

    def count(self) -> int:
        with self._session_factory() as session:
            statement = select(func.count(Usuario.id))
            return int(session.exec(statement).one() or 0)

    def count_presencial(self) -> int:
        with self._session_factory() as session:
            statement = select(func.count(Usuario.id)).where(Usuario.modalidade == "Presencial")
            return int(session.exec(statement).one() or 0)

    def list_all(self) -> List[Usuario]:
        with self._session_factory() as session:
            statement = select(Usuario).order_by(Usuario.id.asc())
            return list(session.exec(statement).all())

    def obter_estatisticas(self, capacidade_maxima: int) -> dict:
        todos = self.list_all()
        total = len(todos)
        presenciais = sum(1 for u in todos if u.modalidade == "Presencial")
        onlines = sum(1 for u in todos if u.modalidade == "Online")
        presentes_dia1 = sum(1 for u in todos if getattr(u, "presenca_dia1", False))
        presentes_dia2 = sum(1 for u in todos if getattr(u, "presenca_dia2", False))
        presentes = sum(1 for u in todos if getattr(u, "presenca_confirmada", False) or getattr(u, "presenca_dia1", False) or getattr(u, "presenca_dia2", False))
        supervisores = sum(1 for u in todos if getattr(u, "role", "") == "supervisor")

        return {
            "total_inscritos": total,
            "capacidade_maxima": capacidade_maxima,
            "vagas_restantes": max(0, capacidade_maxima - total),
            "presenciais": presenciais,
            "onlines": onlines,
            "presentes": presentes,
            "presentes_dia1": presentes_dia1,
            "presentes_dia2": presentes_dia2,
            "supervisores": supervisores,
        }
