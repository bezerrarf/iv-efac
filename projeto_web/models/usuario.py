"""Entidade Usuario para o domínio do evento AstroData 2026."""

from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
import secrets


class Usuario(SQLModel, table=True):
    """Modelo de Participante / Usuário Inscrito no Evento."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    instituicao: str = Field(default="Não informada")
    modalidade: str = Field(default="Presencial")  # 'Presencial' ou 'Online'
    area: str = Field(default="Ciência de Dados / IA")
    senha_hash: str
    codigo_inscricao: str = Field(
        default_factory=lambda: f"ASTRO-{secrets.token_hex(3).upper()}",
        index=True,
    )
    criado_em: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
