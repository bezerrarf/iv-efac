"""Serviço de segurança e criptografia de senhas seguindo SRP e DIP."""

import hashlib
import secrets
from typing import Protocol


class PasswordHasherProtocol(Protocol):
    """Contrato abstrato para serviços de hash de senhas (DIP / OCP)."""

    def hash(self, password: str) -> str:
        """Gera o hash da senha."""
        ...

    def verify(self, password: str, hashed_password: str) -> bool:
        """Verifica se a senha pura confere com o hash."""
        ...


class PBKDF2PasswordHasher(PasswordHasherProtocol):
    """Implementação concreta de hashing com PBKDF2 HMAC SHA-256 e salt seguro."""

    def __init__(self, iterations: int = 100_000):
        self.iterations = iterations

    def hash(self, password: str) -> str:
        salt = secrets.token_hex(16)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            self.iterations,
        )
        return f"{salt}${key.hex()}"

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            salt, key_hex = hashed_password.split("$")
            key = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                self.iterations,
            )
            return secrets.compare_digest(key.hex(), key_hex)
        except Exception:
            return False
