"""Testes unitários (TDD) para o contrato e comportamento do repositório de usuários."""

import pytest
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.base import UsuarioRepositoryProtocol


def test_repository_save_and_find_by_email(in_memory_repo: UsuarioRepositoryProtocol):
    user = Usuario(
        nome="Dra. Vera Rubin",
        email="vera.rubin@astro.org",
        instituicao="Carnegie Institution",
        modalidade="Presencial",
        area="Astrofísica",
        senha_hash="dummy_hash_123",
    )
    saved = in_memory_repo.save(user)
    assert saved.id is not None
    assert saved.codigo_inscricao.startswith("ASTRO-")

    found = in_memory_repo.find_by_email("vera.rubin@astro.org")
    assert found is not None
    assert found.nome == "Dra. Vera Rubin"
    assert found.id == saved.id


def test_repository_case_insensitive_email(in_memory_repo: UsuarioRepositoryProtocol):
    user = Usuario(
        nome="Edwin Hubble",
        email="Hubble@Observatorio.org",
        senha_hash="dummy_hash_456",
    )
    in_memory_repo.save(user)

    found = in_memory_repo.find_by_email("hubble@observatorio.org")
    assert found is not None
    assert found.nome == "Edwin Hubble"


def test_repository_not_found(in_memory_repo: UsuarioRepositoryProtocol):
    found = in_memory_repo.find_by_email("nao_existe@astro.org")
    assert found is None


def test_repository_count_and_list(in_memory_repo: UsuarioRepositoryProtocol):
    assert in_memory_repo.count() == 0
    in_memory_repo.save(Usuario(nome="User 1", email="u1@test.org", senha_hash="h1"))
    in_memory_repo.save(Usuario(nome="User 2", email="u2@test.org", senha_hash="h2"))

    assert in_memory_repo.count() == 2
    assert len(in_memory_repo.list_all()) == 2
