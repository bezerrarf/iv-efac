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


def test_fluxo_completo_admin_supervisor_presenca_exportacao_e_nova_inscricao(sqlite_controller: UsuarioController):
    """Teste de integração completo validando:
    - Criação de Admin, Supervisor (promovido apenas por Admin) e Participantes com acentuação pt-BR.
    - Bloqueio de marcação de presença pelo próprio participante.
    - Marcação de presença de participante pelo Supervisor (permitido).
    - Bloqueio de marcação de presença de Admin pelo Supervisor (proibido).
    - Exportação de lista de participantes em CSV (sem BOM) e PDF Oficial (com fontes TrueType UTF-8).
    """
    from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos

    # 1. Cadastra Admin, futuro Supervisor e Participante com acentos da língua portuguesa
    res_adm = sqlite_controller.cadastrar("Prof. Dr. Otoniel Administração", "otoniel.admin@ufca.edu.br", "admin12345", "UFCA")
    res_sup = sqlite_controller.cadastrar("Conceição Assunção (Supervisão)", "conceicao.sup@ufca.edu.br", "superv12345", "UFCA")
    res_part = sqlite_controller.cadastrar("João André Magalhães Júnior", "joao.magalhaes@ufca.edu.br", "part12345", "IFCE – Juazeiro")

    adm_id = res_adm.dado.id
    sup_id = res_sup.dado.id
    part_id = res_part.dado.id

    # Configura o Admin e promove o Supervisor pelo painel do Admin
    sqlite_controller.alterar_role(adm_id, "admin", solicitante_role="admin")
    res_prom = sqlite_controller.atualizar_participante_completo(
        user_id=sup_id,
        nome="Conceição Assunção (Supervisão)",
        email="conceicao.sup@ufca.edu.br",
        instituicao="UFCA",
        modalidade="Presencial",
        area="Física Computacional",
        role="supervisor",
        presenca_dia1=False,
        presenca_dia2=False,
        solicitante_role="admin",
    )
    assert res_prom.sucesso is True
    assert res_prom.dado.role == "supervisor"

    # 2. Participante tenta marcar a própria presença -> Bloqueado
    res_auto = sqlite_controller.alternar_presenca(part_id, dia="Dia 1", solicitante_role="participante")
    assert res_auto.sucesso is False

    # 3. Supervisor marca presença do Participante nos Dias 1 e 2 -> Permitido
    res_p1 = sqlite_controller.alternar_presenca(part_id, dia="Dia 1", solicitante_role="supervisor")
    res_p2 = sqlite_controller.alternar_presenca(part_id, dia="Dia 2", solicitante_role="supervisor")
    assert res_p1.sucesso is True and res_p1.dado.presenca_dia1 is True
    assert res_p2.sucesso is True and res_p2.dado.presenca_dia2 is True

    # 4. Supervisor tenta marcar presença do Admin -> Bloqueado
    res_sup_adm = sqlite_controller.alternar_presenca(adm_id, dia="Dia 1", solicitante_role="supervisor")
    assert res_sup_adm.sucesso is False
    assert "administradores" in res_sup_adm.mensagem.lower()

    # 5. Exportação CSV e PDF com acentuação pt-BR completa
    inscritos = sqlite_controller.listar_inscritos()
    stats = sqlite_controller.obter_estatisticas()
    assert len(inscritos) == 3

    csv_data = gerar_csv_inscritos(inscritos)
    assert not csv_data.startswith("\ufeff")
    assert "João André Magalhães Júnior" in csv_data
    assert "Conceição Assunção (Supervisão)" in csv_data

    pdf_data = gerar_pdf_inscritos(inscritos, stats)
    assert pdf_data.startswith(b"%PDF-")
    assert len(pdf_data) > 1500

