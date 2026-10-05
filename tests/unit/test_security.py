"""Testes unitários (TDD) para o serviço de criptografia e hashing de senhas."""

import pytest
from projeto_web.core.security import PBKDF2PasswordHasher


def test_hash_generation():
    hasher = PBKDF2PasswordHasher()
    raw_pass = "segredo_astronomico_2026"
    hash1 = hasher.hash(raw_pass)
    hash2 = hasher.hash(raw_pass)

    assert hash1 != raw_pass
    # Salts diferentes produzem hashes diferentes para a mesma senha
    assert hash1 != hash2
    assert "$" in hash1


def test_password_verification_success():
    hasher = PBKDF2PasswordHasher()
    raw_pass = "galaxia_andromeda"
    hashed = hasher.hash(raw_pass)

    assert hasher.verify(raw_pass, hashed) is True


def test_password_verification_failure():
    hasher = PBKDF2PasswordHasher()
    raw_pass = "telescopio_james_webb"
    hashed = hasher.hash(raw_pass)

    assert hasher.verify("senha_incorreta", hashed) is False
    assert hasher.verify("", hashed) is False


def test_invalid_hash_format_handling():
    hasher = PBKDF2PasswordHasher()
    assert hasher.verify("senha", "hash_invalido_sem_cifrao") is False
