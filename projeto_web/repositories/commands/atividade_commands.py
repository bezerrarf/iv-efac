"""Comandos de escrita para atividades no padrão CQRS (Command Side)."""

from typing import Optional
from sqlmodel import Session, select
from projeto_web.models.atividade import AtividadeModel
from projeto_web.repositories.base import AtividadeCommandRepositoryProtocol
from projeto_web.repositories.database import get_session


class SQLiteAtividadeCommandRepository(AtividadeCommandRepositoryProtocol):
    def __init__(self, session_factory=get_session):
        self._session_factory = session_factory

    def create(self, atividade: AtividadeModel) -> AtividadeModel:
        with self._session_factory() as session:
            session.add(atividade)
            session.commit()
            session.refresh(atividade)
            return atividade

    def update(self, atividade: AtividadeModel) -> Optional[AtividadeModel]:
        with self._session_factory() as session:
            merged = session.merge(atividade)
            session.commit()
            session.refresh(merged)
            return merged

    def update_by_fields(
        self,
        id: int,
        dia: str,
        horario: str,
        titulo: str,
        palestrante: str,
        local: str,
        tipo: str,
        descricao: str,
    ) -> bool:
        with self._session_factory() as session:
            item = session.get(AtividadeModel, id)
            if not item:
                return False
            item.dia = dia
            item.horario = horario
            item.titulo = titulo
            item.palestrante = palestrante
            item.local = local
            item.tipo = tipo
            item.descricao = descricao
            session.add(item)
            session.commit()
            return True

    def delete(self, atividade_id: int) -> bool:
        with self._session_factory() as session:
            item = session.get(AtividadeModel, atividade_id)
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

    def clear_all(self) -> bool:
        with self._session_factory() as session:
            itens = session.exec(select(AtividadeModel)).all()
            for i in itens:
                session.delete(i)
            session.commit()
            return True
