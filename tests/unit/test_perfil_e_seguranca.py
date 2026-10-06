"""Testes unitários para Edição de Perfil, Troca de Senha, Confirmação de E-mail e Emissão de Carteirinha PNG."""

import pytest
from sqlmodel import create_engine, SQLModel, Session
from projeto_web.models.usuario import Usuario
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.core.badge_service import BadgeService
from projeto_web.core.quotes_service import carregar_frases_cientistas


@pytest.fixture
def repo_teste():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return SQLiteUsuarioRepository(session_factory=lambda: Session(engine))


@pytest.fixture
def controller_teste(repo_teste):
    return UsuarioController(
        repository=repo_teste,
        hasher=PBKDF2PasswordHasher(),
        capacidade_maxima=100,
    )


def test_atualizar_perfil(controller_teste):
    # 1. Cadastra usuário
    cad = controller_teste.cadastrar(
        nome="Cientista Teste",
        email="cientista@ufca.edu.br",
        senha="Senha123!",
        instituicao="UFCA Brejo Santo",
        modalidade="Presencial",
    )
    assert cad.sucesso
    u_id = cad.dado.id

    # 2. Atualiza perfil
    res = controller_teste.atualizar_perfil(
        user_id=u_id,
        nome="Cientista Doutor Teste",
        instituicao="Universidade Federal do Cariri (Campus Brejo Santo)",
        modalidade="Online",
    )
    assert res.sucesso
    assert res.dado.nome == "Cientista Doutor Teste"
    assert res.dado.instituicao == "Universidade Federal do Cariri (Campus Brejo Santo)"
    assert res.dado.modalidade == "Online"


def test_alterar_minha_senha_sucesso_e_falha(controller_teste):
    # 1. Cadastra usuário
    cad = controller_teste.cadastrar(
        nome="Admin Segurança",
        email="admin.seg@ufca.edu.br",
        senha="SenhaAtual123!",
    )
    assert cad.sucesso
    u_id = cad.dado.id

    # 2. Falha com senha atual incorreta
    res_err = controller_teste.alterar_minha_senha(
        user_id=u_id,
        senha_atual="SenhaIncorreta",
        nova_senha="NovaSenha456!",
        confirma_senha="NovaSenha456!",
    )
    assert not res_err.sucesso
    assert "Senha atual incorreta" in res_err.mensagem

    # 3. Falha quando senhas não coincidem
    res_diverg = controller_teste.alterar_minha_senha(
        user_id=u_id,
        senha_atual="SenhaAtual123!",
        nova_senha="NovaSenha456!",
        confirma_senha="OutraSenhaDiferente",
    )
    assert not res_diverg.sucesso
    assert "não coincidem" in res_diverg.mensagem

    # 4. Sucesso ao informar credenciais corretas
    res_ok = controller_teste.alterar_minha_senha(
        user_id=u_id,
        senha_atual="SenhaAtual123!",
        nova_senha="NovaSenha456!",
        confirma_senha="NovaSenha456!",
    )
    assert res_ok.sucesso

    # 5. Valida que login com a nova senha funciona
    login_ok = controller_teste.autenticar("admin.seg@ufca.edu.br", "NovaSenha456!")
    assert login_ok.sucesso


def test_confirmacao_email_fluxo(controller_teste):
    # 1. Cadastra usuário com email inicialmente não confirmado
    cad = controller_teste.cadastrar(
        nome="Participante Artigo",
        email="artigo@ufca.edu.br",
        senha="Senha123!",
    )
    assert cad.sucesso
    u_id = cad.dado.id
    assert cad.dado.email_confirmado is False

    # 2. Gera código de 6 dígitos
    cod_res = controller_teste.gerar_codigo_confirmacao(u_id)
    assert cod_res.sucesso
    assert len(cod_res.dado) == 6
    codigo_gerado = cod_res.dado

    # 3. Tentativa com código incorreto
    err_conf = controller_teste.confirmar_email(u_id, codigo="000000")
    assert not err_conf.sucesso
    assert "Código de confirmação incorreto" in err_conf.mensagem

    # 4. Confirmação com o código correto
    ok_conf = controller_teste.confirmar_email(u_id, codigo=codigo_gerado)
    assert ok_conf.sucesso
    assert ok_conf.dado.email_confirmado is True


def test_gerador_carteirinha_png():
    # Valida geração oficial da imagem PNG da carteirinha
    img_bytes = BadgeService.gerar_imagem_carteirinha(
        nome="Ramon Firmino Bezerra",
        email="ramon@ufca.edu.br",
        instituicao="Universidade Federal do Cariri (UFCA)",
        modalidade="Presencial",
        role="admin",
        codigo="ADMIN-001",
        email_confirmado=True,
        base_assets_path="assets",
    )
    assert isinstance(img_bytes, bytes)
    assert len(img_bytes) > 50000
    # Magic bytes de arquivo PNG
    assert img_bytes[:8] == b"\x89PNG\r\n\x1a\n"


def test_carregamento_frases_cientistas():
    # Valida leitura e parsing do arquivo frases_cientistas.txt
    frases = carregar_frases_cientistas("frases_cientistas.txt")
    assert isinstance(frases, list)
    assert len(frases) >= 8
    for f in frases:
        assert "autor" in f and len(f["autor"]) > 0
        assert "area" in f
        assert "icone" in f
        assert "cor" in f and f["cor"].startswith("#")
        assert "frase" in f and len(f["frase"]) > 10
