"""Camada de Acesso a Dados e Repositórios no Padrão CQRS (Command Query Responsibility Segregation)."""

from .base import (
    UsuarioCommandRepositoryProtocol,
    UsuarioQueryRepositoryProtocol,
    UsuarioRepositoryProtocol,
    AtividadeCommandRepositoryProtocol,
    AtividadeQueryRepositoryProtocol,
)
from .commands.usuario_commands import SQLiteUsuarioCommandRepository
from .queries.usuario_queries import SQLiteUsuarioQueryRepository
from .commands.atividade_commands import SQLiteAtividadeCommandRepository
from .queries.atividade_queries import SQLiteAtividadeQueryRepository
from .sqlite_usuario import SQLiteUsuarioRepository

__all__ = [
    "UsuarioCommandRepositoryProtocol",
    "UsuarioQueryRepositoryProtocol",
    "UsuarioRepositoryProtocol",
    "AtividadeCommandRepositoryProtocol",
    "AtividadeQueryRepositoryProtocol",
    "SQLiteUsuarioCommandRepository",
    "SQLiteUsuarioQueryRepository",
    "SQLiteAtividadeCommandRepository",
    "SQLiteAtividadeQueryRepository",
    "SQLiteUsuarioRepository",
]
