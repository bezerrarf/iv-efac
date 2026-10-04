"""Configurações e fixtures globais de teste para o AstroData 2026."""

import pytest
from typing import Optional
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioRepositoryProtocol
from projeto_web.core.security import PasswordHasherProtocol, PBKDF2PasswordHasher


class InMemoryUsuarioRepository(UsuarioRepositoryProtocol):
    """Implementação em memória do repositório para testes unitários isolados (LSP/DIP)."""

    def __init__(self):
        self._usuarios: dict[int, Usuario] = {}
        self._next_id: int = 1

    def save(self, usuario: Usuario) -> Usuario:
        if usuario.id is None:
            usuario.id = self._next_id
            self._next_id += 1
        self._usuarios[usuario.id] = usuario
        return usuario

    def find_by_email(self, email: str) -> Optional[Usuario]:
        email_clean = email.strip().lower()
        for u in self._usuarios.values():
            if u.email.strip().lower() == email_clean:
                return u
        return None

    def find_by_id(self, user_id: int) -> Optional[Usuario]:
        return self._usuarios.get(user_id)

    def count(self) -> int:
        return len(self._usuarios)

    def list_all(self) -> list[Usuario]:
        return list(self._usuarios.values())


@pytest.fixture
def hasher() -> PasswordHasherProtocol:
    """Fixture para o serviço de hashing seguro."""
    return PBKDF2PasswordHasher()


@pytest.fixture
def in_memory_repo() -> UsuarioRepositoryProtocol:
    """Fixture para o repositório em memória."""
    return InMemoryUsuarioRepository()
