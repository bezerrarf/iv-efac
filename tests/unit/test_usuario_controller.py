"""Testes unitários (TDD) para o Controller de Usuário com injeção de dependências (DIP)."""

import pytest
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.repositories.base import UsuarioRepositoryProtocol
from projeto_web.core.security import PasswordHasherProtocol


@pytest.fixture
def controller(in_memory_repo: UsuarioRepositoryProtocol, hasher: PasswordHasherProtocol) -> UsuarioController:
    return UsuarioController(repository=in_memory_repo, hasher=hasher)


def test_cadastro_sucesso(controller: UsuarioController):
    result = controller.cadastrar(
        nome="Carl Sagan",
        email="carl.sagan@cornell.edu",
        senha="bilhoes_e_bilhoes",
        instituicao="Cornell",
        modalidade="Presencial",
        area="Cosmologia",
    )
    assert result.sucesso is True
    assert result.dado is not None
    assert result.dado.nome == "Carl Sagan"
    assert result.dado.codigo_inscricao.startswith("ASTRO-")
    assert result.mensagem == "Inscrição realizada com sucesso!"


def test_cadastro_campos_obrigatorios(controller: UsuarioController):
    res1 = controller.cadastrar(nome="", email="carl@test.org", senha="123456")
    assert res1.sucesso is False
    assert "Nome, e-mail e senha são obrigatórios" in res1.mensagem

    res2 = controller.cadastrar(nome="Carl", email="", senha="123456")
    assert res2.sucesso is False

    res3 = controller.cadastrar(nome="Carl", email="carl@test.org", senha="123")
    assert res3.sucesso is False
    assert "mínimo 6 caracteres" in res3.mensagem


def test_cadastro_email_duplicado(controller: UsuarioController):
    controller.cadastrar(
        nome="Johannes Kepler",
        email="kepler@astro.org",
        senha="leis_de_kepler",
    )
    res_duplicado = controller.cadastrar(
        nome="Outro Kepler",
        email="KEPLER@astro.org",
        senha="outra_senha_qualquer",
    )
    assert res_duplicado.sucesso is False
    assert "já está cadastrado" in res_duplicado.mensagem


def test_autenticacao_sucesso(controller: UsuarioController):
    controller.cadastrar(
        nome="Galileo Galilei",
        email="galileo@padua.it",
        senha="luneta_revolucionaria",
    )
    res = controller.autenticar(email="galileo@padua.it", senha="luneta_revolucionaria")
    assert res.sucesso is True
    assert res.dado is not None
    assert res.dado.nome == "Galileo Galilei"


def test_autenticacao_senha_invalida(controller: UsuarioController):
    controller.cadastrar(
        nome="Galileo Galilei",
        email="galileo@padua.it",
        senha="luneta_revolucionaria",
    )
    res = controller.autenticar(email="galileo@padua.it", senha="senha_errada")
    assert res.sucesso is False
    assert "Senha incorreta" in res.mensagem


def test_autenticacao_usuario_inexistente(controller: UsuarioController):
    res = controller.autenticar(email="inexistente@astro.org", senha="qualquer_senha")
    assert res.sucesso is False
    assert "não encontrado" in res.mensagem


def test_alterar_modalidade(controller: UsuarioController):
    cadastro = controller.cadastrar(
        nome="Stephen Hawking",
        email="hawking@cambridge.ac.uk",
        senha="buracos_negros",
        modalidade="Presencial",
    )
    user_id = cadastro.dado.id

    res_alteracao = controller.alterar_modalidade(user_id=user_id, nova_modalidade="Online")
    assert res_alteracao.sucesso is True
    assert res_alteracao.dado.modalidade == "Online"


def test_obter_estatisticas(controller: UsuarioController):
    stats1 = controller.obter_estatisticas()
    assert stats1["total_inscritos"] == 0
    assert stats1["vagas_restantes"] == 300

    controller.cadastrar(nome="U1", email="u1@test.org", senha="senha123")
    controller.cadastrar(nome="U2", email="u2@test.org", senha="senha123")

    stats2 = controller.obter_estatisticas()
    assert stats2["total_inscritos"] == 2
    assert stats2["vagas_restantes"] == 298


def test_promover_e_revogar_supervisor(controller: UsuarioController):
    cadastro = controller.cadastrar(
        nome="Vera Rubin",
        email="vera.rubin@carnegie.edu",
        senha="materia_escura",
    )
    user_id = cadastro.dado.id
    assert cadastro.dado.role == "participante"

    # Promover a supervisor
    res_promocao = controller.alterar_role(user_id, "supervisor")
    assert res_promocao.sucesso is True
    assert res_promocao.dado.role == "supervisor"
    assert "Supervisor" in res_promocao.mensagem

    # Revogar para participante
    res_revogacao = controller.alterar_role(user_id, "participante")
    assert res_revogacao.sucesso is True
    assert res_revogacao.dado.role == "participante"


def test_conferencia_presenca(controller: UsuarioController):
    cadastro = controller.cadastrar(
        nome="Jocelyn Bell Burnell",
        email="jocelyn.bell@oxford.ac.uk",
        senha="pulsar_descobe",
    )
    user_id = cadastro.dado.id
    assert cadastro.dado.presenca_confirmada is False

    # Marcar presença (Check-in)
    res_presenca1 = controller.alternar_presenca(user_id)
    assert res_presenca1.sucesso is True
    assert res_presenca1.dado.presenca_confirmada is True
    assert "CONFIRMADA" in res_presenca1.mensagem

    # Desmarcar presença
    res_presenca2 = controller.alternar_presenca(user_id)
    assert res_presenca2.sucesso is True
    assert res_presenca2.dado.presenca_confirmada is False
    assert "PENDENTE" in res_presenca2.mensagem


def test_atualizar_foto_perfil(controller: UsuarioController):
    cadastro = controller.cadastrar(
        nome="Albert Einstein",
        email="einstein@princeton.edu",
        senha="relatividade_geral",
    )
    user_id = cadastro.dado.id

    res_foto = controller.atualizar_foto(user_id, "https://exemplo.com/foto_einstein.jpg")
    assert res_foto.sucesso is True
    assert res_foto.dado.foto_url == "https://exemplo.com/foto_einstein.jpg"


def test_listar_inscritos_com_filtro(controller: UsuarioController):
    controller.cadastrar(nome="Max Planck", email="planck@berlin.de", senha="quanta_de_energia", instituicao="Univ Berlim")
    controller.cadastrar(nome="Niels Bohr", email="bohr@copenhagen.dk", senha="modelo_atomico", instituicao="Univ Copenhague")

    # Sem filtro: retorna todos
    todos = controller.listar_inscritos()
    assert len(todos) == 2

    # Com filtro por nome
    filtro_planck = controller.listar_inscritos("Planck")
    assert len(filtro_planck) == 1
    assert filtro_planck[0].nome == "Max Planck"

    # Com filtro por instituicao
    filtro_inst = controller.listar_inscritos("Copenhague")
    assert len(filtro_inst) == 1
    assert filtro_inst[0].nome == "Niels Bohr"


def test_alterar_senha_sucesso_e_validacao(controller: UsuarioController):
    res_cad = controller.cadastrar(
        nome="Richard Feynman",
        email="feynman@caltech.edu",
        senha="senha_antiga_123",
        instituicao="Caltech",
    )
    user_id = res_cad.dado.id

    # Teste de validação (senha muito curta)
    res_curta = controller.alterar_senha(user_id, "12345")
    assert not res_curta.sucesso
    assert "mínimo 6" in res_curta.mensagem

    # Teste de sucesso
    res_alt = controller.alterar_senha(user_id, "Quantum_Electrodynamics_2026!")
    assert res_alt.sucesso
    assert "atualizada com sucesso" in res_alt.mensagem

    # Autenticar com a nova senha
    res_login_novo = controller.autenticar("feynman@caltech.edu", "Quantum_Electrodynamics_2026!")
    assert res_login_novo.sucesso

    # Tentativa com senha antiga deve falhar
    res_login_velho = controller.autenticar("feynman@caltech.edu", "senha_antiga_123")
    assert not res_login_velho.sucesso


def test_export_service_csv_e_pdf(controller: UsuarioController):
    from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos

    controller.cadastrar(nome="Ada Lovelace", email="ada@analytical.uk", senha="bernoulli_numbers", instituicao="London")
    usuarios = controller.listar_inscritos()
    stats = controller.obter_estatisticas()

    # Validação do CSV
    csv_str = gerar_csv_inscritos(usuarios)
    assert "Ada Lovelace" in csv_str
    assert "ada@analytical.uk" in csv_str
    assert "London" in csv_str

    # Validação do PDF
    pdf_bytes = gerar_pdf_inscritos(usuarios, stats)
    assert len(pdf_bytes) > 500
    assert pdf_bytes.startswith(b"%PDF-")
