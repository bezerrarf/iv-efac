"""Modelo persistente da grade de programação e atividades do IV EFAC."""

from typing import Optional
from sqlmodel import Field, SQLModel


class AtividadeModel(SQLModel, table=True):
    """Modelo de Atividade / Palestra persistido no SQLite."""

    id: Optional[int] = Field(default=None, primary_key=True)
    dia: str = Field(index=True)  # 'Dia 1' ou 'Dia 2'
    horario: str
    titulo: str
    palestrante: str
    local: str
    tipo: str
    descricao: str
    tipo_color: str = Field(default="indigo")
    ordem: int = Field(default=0)
