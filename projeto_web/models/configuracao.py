"""Modelo de dados para configurações e links dinâmicos do evento."""

from typing import Optional
from sqlmodel import Field, SQLModel


class ConfiguracaoModel(SQLModel, table=True):
    chave: str = Field(primary_key=True)
    valor: str
