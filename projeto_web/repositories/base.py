"""Contratos e interfaces abstratas para persistência de dados (ISP / DIP)."""

from typing import Optional, Protocol
from projeto_web.models.usuario import Usuario


class UsuarioRepositoryProtocol(Protocol):
    """Contrato abstrato para repositórios de usuários (DIP)."""

    def save(self, usuario: Usuario) -> Usuario:
        """Salva ou atualiza um usuário no repositório."""
        ...

    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Localiza um usuário pelo seu e-mail (case-insensitive)."""
        ...

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        """Localiza um usuário pelo seu ID."""
        ...

    def count(self) -> int:
        """Retorna a contagem total de usuários cadastrados."""
        ...

    def list_all(self) -> list[Usuario]:
        """Retorna todos os usuários cadastrados."""
        ...
