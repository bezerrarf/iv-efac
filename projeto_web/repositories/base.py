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

    def update_role(self, user_id: int, role: str) -> Optional[Usuario]:
        """Atualiza a role/permissão de um usuário ('participante', 'supervisor', 'admin')."""
        ...

    def toggle_presenca(self, user_id: int) -> Optional[Usuario]:
        """Alterna o status de presença confirmada de um participante."""
        ...

    def update_foto(self, user_id: int, foto_url: str) -> Optional[Usuario]:
        """Atualiza a URL ou dado da foto do participante."""
        ...

    def update_senha(self, user_id: int, nova_senha_hash: str) -> Optional[Usuario]:
        """Atualiza a senha criptografada (hash PBKDF2) de um usuário."""
        ...
