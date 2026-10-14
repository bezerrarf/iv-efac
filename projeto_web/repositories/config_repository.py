"""Acesso a configurações persistentes no padrão CQRS."""

from typing import Optional
from sqlmodel import Session, select
from projeto_web.models.configuracao import ConfiguracaoModel
from projeto_web.repositories.database import get_session


class ConfigRepository:
    """Repositório de chave-valor para configurações dinâmicas do evento."""

    def __init__(self, session_factory=get_session):
        self._session_factory = session_factory

    def get(self, chave: str, default: str = "") -> str:
        with self._session_factory() as session:
            item = session.get(ConfiguracaoModel, chave)
            if item:
                return item.valor
            return default

    def set(self, chave: str, valor: str) -> None:
        with self._session_factory() as session:
            item = session.get(ConfiguracaoModel, chave)
            if item:
                item.valor = valor
                session.add(item)
            else:
                novo = ConfiguracaoModel(chave=chave, valor=valor)
                session.add(novo)
            session.commit()
