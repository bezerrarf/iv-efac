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

def test_excluir_participante_sucesso_e_inexistente(controller: UsuarioController):
    res_cad = controller.cadastrar(
        nome="Alan Turing",
        email="turing@bletchley.uk",
        senha="enigma_cracker",
        instituicao="Cambridge",
    )
    assert res_cad.sucesso
    user_id = res_cad.dado.id

    # Exclusão com sucesso (exclusivo para admin)
    res_del = controller.excluir_participante(user_id, solicitante_role="admin")
    assert res_del.sucesso
    assert "excluído com sucesso" in res_del.mensagem

    # Confirmar que não é mais encontrado
    assert controller._queries.find_by_id(user_id) is None

    # Tentar excluir novamente deve retornar insucesso
    res_del2 = controller.excluir_participante(user_id, solicitante_role="admin")
    assert not res_del2.sucesso
    assert "não encontrado" in res_del2.mensagem


def test_excluir_participante_bloqueado_para_nao_admin(controller: UsuarioController):
    """Garante que apenas administradores podem excluir contatos."""
    res_cad = controller.cadastrar(
        nome="Participante Protegido",
        email="protegido@ufca.edu.br",
        senha="senha_segura_123",
        instituicao="UFCA",
    )
    assert res_cad.sucesso
    uid = res_cad.dado.id

    for role_invalida in ["participante", "supervisor", ""]:
        res_negado = controller.excluir_participante(uid, solicitante_role=role_invalida)
        assert res_negado.sucesso is False
        assert "somente administradores" in res_negado.mensagem
        assert controller._queries.find_by_id(uid) is not None


def test_autenticacao_tolerante_a_espacos_e_caixa_alta(controller: UsuarioController):
    """Garante que inscritos conseguem acessar seu cadastro mesmo com letras maiúsculas ou espaços do teclado móvel."""
    res_cad = controller.cadastrar(
        nome="Inscrito Mobile",
        email="Mobile.User@UFCA.edu.br",
        senha="SenhaMobile123",
    )
    assert res_cad.sucesso

    # Login com e-mail em maiúsculas e espaço acidental no final da senha
    res_auth = controller.autenticar("  MOBILE.USER@UFCA.EDU.BR  ", "SenhaMobile123 ")
    assert res_auth.sucesso is True
    assert res_auth.dado.nome == "Inscrito Mobile"


def test_regras_presenca_participante_supervisor_admin(controller: UsuarioController):
    """Garante que:
    1. Participantes comuns NÃO podem marcar sua própria presença.
    2. Supervisores PODEM marcar presença de participantes e supervisores, EXCETO de Admins.
    3. Admins PODEM marcar presença de qualquer pessoa (incluindo Admins).
    """
    cad_part = controller.cadastrar("João Participante", "joao@ufca.edu.br", "senha123")
    cad_admin = controller.cadastrar("Maria Admin", "admin@ufca.edu.br", "senha123")
    controller.alterar_role(cad_admin.dado.id, "admin", solicitante_role="admin")

    # 1. Participante comum bloqueado
    res_negado_part = controller.alternar_presenca(cad_part.dado.id, dia="Dia 1", solicitante_role="participante")
    assert res_negado_part.sucesso is False
    assert "não podem marcar a própria presença" in res_negado_part.mensagem

    # 2. Supervisor marca presença de participante comum -> Sucesso
    res_sup_ok = controller.alternar_presenca(cad_part.dado.id, dia="Dia 1", solicitante_role="supervisor")
    assert res_sup_ok.sucesso is True
    assert res_sup_ok.dado.presenca_dia1 is True

    # 3. Supervisor tenta marcar presença de um Admin -> Bloqueado
    res_sup_admin = controller.alternar_presenca(cad_admin.dado.id, dia="Dia 1", solicitante_role="supervisor")
    assert res_sup_admin.sucesso is False
    assert "administradores" in res_sup_admin.mensagem.lower()

    # 4. Admin marca presença de Admin -> Sucesso
    res_adm_admin = controller.alternar_presenca(cad_admin.dado.id, dia="Dia 1", solicitante_role="admin")
    assert res_adm_admin.sucesso is True
    assert res_adm_admin.dado.presenca_dia1 is True


def test_apenas_admin_pode_conceder_permissao_supervisor(controller: UsuarioController):
    """Garante que somente Admin pode alterar role ou promover usuário a Supervisor."""
    cad = controller.cadastrar("Carlos Candidato", "carlos@ufca.edu.br", "senha123")
    uid = cad.dado.id

    # Supervisor ou participante não pode promover ninguém
    for role_nao_admin in ["participante", "supervisor"]:
        res_negado = controller.alterar_role(uid, "supervisor", solicitante_role=role_nao_admin)
        assert res_negado.sucesso is False
        assert "somente administradores" in res_negado.mensagem

    # Admin promove a supervisor via atualizar_participante_completo
    res_ok = controller.atualizar_participante_completo(
        user_id=uid,
        nome="Carlos Supervisor",
        email="carlos@ufca.edu.br",
        instituicao="UFCA",
        modalidade="Presencial",
        area="Astrofísica",
        role="supervisor",
        presenca_dia1=True,
        presenca_dia2=False,
        solicitante_role="admin",
    )
    assert res_ok.sucesso is True
    assert res_ok.dado.role == "supervisor"
    assert res_ok.dado.presenca_dia1 is True


def test_acentuacao_ptbr_nfc_e_csv_sem_bom_ios(controller: UsuarioController):
    """Garante que acentos pt-BR (NFD do iOS/macOS) são normalizados para NFC e o CSV não possui BOM \\ufeff."""
    import unicodedata
    from projeto_web.core.export_service import gerar_csv_inscritos, gerar_pdf_inscritos

    # Texto decomposto (NFD) simulando entrada de teclado iOS/Safari + caractere fantasma \ufeff
    nome_nfd = "\ufeff" + unicodedata.normalize("NFD", "João André Conceição Assunção Magalhães")
    inst_nfd = unicodedata.normalize("NFD", "Instituição de Pós-Graduação em Ciências Físicas – São Paulo")

    res = controller.cadastrar(
        nome=nome_nfd,
        email="joao.andre@ufca.edu.br",
        senha="senha_acento_123",
        instituicao=inst_nfd,
        modalidade="Presencial",
        area="Relatividade e Gravitação",
    )
    assert res.sucesso is True
    assert res.dado.nome == "João André Conceição Assunção Magalhães"
    assert unicodedata.is_normalized("NFC", res.dado.nome)
    assert "\ufeff" not in res.dado.nome

    usuarios = controller.listar_inscritos()
    csv_str = gerar_csv_inscritos(usuarios)
    # Sem BOM no início para não travar WebKit/JavaScriptCore no iPhone
    assert not csv_str.startswith("\ufeff")
    assert "\ufeff" not in csv_str
    assert "João André Conceição Assunção Magalhães" in csv_str

    pdf_bytes = gerar_pdf_inscritos(usuarios, controller.obter_estatisticas())
    assert pdf_bytes.startswith(b"%PDF-")
    assert len(pdf_bytes) > 1000


