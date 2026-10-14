"""Consultas de leitura para atividades no padrão CQRS."""

from typing import List
from sqlmodel import Session, select
from projeto_web.models.atividade import AtividadeModel
from projeto_web.repositories.base import AtividadeQueryRepositoryProtocol
from projeto_web.repositories.database import get_session


class SQLiteAtividadeQueryRepository(AtividadeQueryRepositoryProtocol):
    def __init__(self, session_factory=get_session):
        self._session_factory = session_factory

    def find_by_dia(self, dia: str) -> List[AtividadeModel]:
        with self._session_factory() as session:
            stmt = (
                select(AtividadeModel)
                .where(AtividadeModel.dia == dia)
                .order_by(AtividadeModel.ordem.asc(), AtividadeModel.id.asc())
            )
            return list(session.exec(stmt).all())

    def list_all(self) -> List[AtividadeModel]:
        with self._session_factory() as session:
            stmt = select(AtividadeModel).order_by(AtividadeModel.dia.asc(), AtividadeModel.ordem.asc())
            return list(session.exec(stmt).all())

    def count(self) -> int:
        with self._session_factory() as session:
            stmt = select(AtividadeModel)
            return len(session.exec(stmt).all())
