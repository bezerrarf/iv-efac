"""Fachada do Repositório de Usuários no SQLite integrando Commands e Queries (CQRS / DIP)."""

from projeto_web.repositories.base import UsuarioRepositoryProtocol
from projeto_web.repositories.commands.usuario_commands import SQLiteUsuarioCommandRepository
from projeto_web.repositories.queries.usuario_queries import SQLiteUsuarioQueryRepository
from projeto_web.repositories.database import get_session


class SQLiteUsuarioRepository(
    SQLiteUsuarioCommandRepository,
    SQLiteUsuarioQueryRepository,
    UsuarioRepositoryProtocol,
):
    """Repositório de usuários unificando CQRS através de especialização de comandos e consultas."""

    def __init__(self, session_factory=get_session):
        SQLiteUsuarioCommandRepository.__init__(self, session_factory=session_factory)
        SQLiteUsuarioQueryRepository.__init__(self, session_factory=session_factory)
