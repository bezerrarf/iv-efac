"""Testes de integração: SQLite real, modo WAL e fluxo completo de ponta a ponta."""

import os
import pytest
from sqlmodel import Session, SQLModel, create_engine
from projeto_web.models.usuario import Usuario
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController


@pytest.fixture
def sqlite_controller(tmp_path):
    """Cria uma base SQLite temporária e isolada para o teste de integração."""
    db_file = tmp_path / "test_evento.db"
    test_db_url = f"sqlite:///{db_file}"
    test_engine = create_engine(test_db_url, connect_args={"check_same_thread": False})

    SQLModel.metadata.create_all(test_engine)
    with test_engine.connect() as conn:
        conn.exec_driver_sql("PRAGMA journal_mode=WAL;")

    def session_factory():
        return Session(test_engine)

    repo = SQLiteUsuarioRepository(session_factory=session_factory)
    hasher = PBKDF2PasswordHasher()
    return UsuarioController(repository=repo, hasher=hasher)


def test_fluxo_integracao_completo(sqlite_controller: UsuarioController):
    # 1. Cadastro inicial
    email = "vera.rubin@telescopio.org"
    res_cad = sqlite_controller.cadastrar(
        nome="Dra. Vera Rubin",
        email=email,
        senha="materia_escura_123",
        instituicao="Observatório Rubin",
        modalidade="Presencial",
        area="Astrofísica",
    )
    assert res_cad.sucesso is True
    assert res_cad.dado is not None
    user_id = res_cad.dado.id
    assert user_id is not None
    assert res_cad.dado.codigo_inscricao.startswith("ASTRO-")

    # 2. Login com credenciais válidas
    res_login = sqlite_controller.autenticar(email=email, senha="materia_escura_123")
    assert res_login.sucesso is True
    assert res_login.dado.nome == "Dra. Vera Rubin"

    # 3. Alteração de modalidade persistida no banco
    res_mod = sqlite_controller.alterar_modalidade(user_id=user_id, nova_modalidade="Online")
    assert res_mod.sucesso is True
    assert res_mod.dado.modalidade == "Online"

    # 4. Verificação de estatísticas
    stats = sqlite_controller.obter_estatisticas()
    assert stats["total_inscritos"] == 1
    assert stats["vagas_restantes"] == 299
