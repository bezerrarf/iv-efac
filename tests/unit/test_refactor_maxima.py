from pathlib import Path
import pytest
import types
import uuid
import reflex as rx
from projeto_web.controllers.evento_controller import EventoController
from projeto_web.state.auth_state import AuthState
from projeto_web.state.admin_state import AdminState
from projeto_web.repositories.sqlite_usuario import SQLiteUsuarioRepository
from projeto_web.core.security import PBKDF2PasswordHasher
from projeto_web.controllers.usuario_controller import UsuarioController
from projeto_web.styles.theme import (
    COLOR_BG,
    COLOR_TEXT_PRIMARY,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)


def test_palestrantes_possuem_fotos_webp():
    """Valida se todos os palestrantes possuem fotos no formato WebP adaptativo."""
    palestrantes = EventoController.obter_palestrantes()
    assert len(palestrantes) == 8
    for p in palestrantes:
        assert hasattr(p, "foto")
        assert p.foto.endswith(".webp") and p.foto.startswith("/participantes/")


def test_participantes_webp_existentes_em_disco():
    """Valida que todos os arquivos WebP gerados existem em participantes/ e assets/participantes/."""
    nomes = [
        "cesar_lenzi",
        "ronaldo_lobato",
        "eliane_angela",
        "iarley_lobo",
        "jonathan_reboucas",
        "celio_muniz",
        "marcos_barros",
        "jose_crisanto",
    ]
    p_dir = Path("participantes")
    assets_dir = Path("assets/participantes")
    
    for n in nomes:
        file_p = p_dir / f"{n}.webp"
        file_a = assets_dir / f"{n}.webp"
        assert file_p.exists(), f"Arquivo WebP não encontrado em participantes: {file_p}"
        assert file_a.exists(), f"Arquivo WebP não encontrado em assets: {file_a}"
        assert file_p.stat().st_size > 5000, f"Arquivo WebP inválido/muito pequeno: {file_p}"


def test_zoom_e_sinergia_estilos():
    """Valida que os estilos globais de texto e tema possuem regras para imunidade a zoom e contraste."""
    assert "text_wrap" in STYLE_HEADING_RESPONSIVE
    assert "overflow_wrap" in STYLE_HEADING_RESPONSIVE
    assert "text_wrap" in STYLE_TEXT_RESPONSIVE
    assert "overflow_wrap" in STYLE_TEXT_RESPONSIVE
    assert Path("assets/styles.css").exists()


def test_auth_state_toggle_mostrar_senha_login():
    """Valida o toggle de visualização de senha no login."""
    state = AuthState()
    assert state.mostrar_senha_login is False
    state.toggle_mostrar_senha_login()
    assert state.mostrar_senha_login is True
    state.toggle_mostrar_senha_login()
    assert state.mostrar_senha_login is False


def test_admin_state_alterar_senha_usuario():
    """Valida a redefinição de senha de usuários pelo administrador."""
    hasher = PBKDF2PasswordHasher()
    repo = SQLiteUsuarioRepository()
    controller = UsuarioController(repository=repo, hasher=hasher)
    
    # Criar usuário de teste com e-mail único
    email_teste = f"user_{uuid.uuid4().hex[:8]}@ufca.edu.br"
    res_cad = controller.cadastrar(
        nome="User TDD Pwd",
        email=email_teste,
        senha="SenhaAntiga123!",
        instituicao="UFCA",
        modalidade="Presencial",
        area="Astrofísica"
    )
    assert res_cad.sucesso
    user_id = res_cad.dado.id

    dummy = types.SimpleNamespace(
        is_admin=True,
        admin_senha_user_id=user_id,
        admin_nova_senha_input="NovaSenhaAdmin456!",
        feedback_msg="",
        feedback_tipo="",
        modal_alterar_senha_aberto=True,
    )
    
    # Em Reflex, métodos decorados como event handlers possuem o callable interno em .fn
    AdminState.salvar_nova_senha_inscrito.fn(dummy)
    assert dummy.feedback_tipo == "success"
    assert dummy.modal_alterar_senha_aberto is False
    
    # Validar se a senha foi atualizada no banco
    auth_check = controller.autenticar(email_teste, "NovaSenhaAdmin456!")
    assert auth_check.sucesso, "Nova senha não autentica após alteração pelo admin"


def test_componentes_novos_sao_reflex():
    """Valida que os novos componentes da Landing Page e Hub são componentes válidos Reflex."""
    from projeto_web.views.components.quick_nav import quick_nav
    from projeto_web.views.components.inscricao_sections.logged_in_hub import logged_in_hub
    from projeto_web.views.pages.home import home_page
    
    assert isinstance(quick_nav(), rx.Component)
    assert isinstance(logged_in_hub(), rx.Component)
    assert isinstance(home_page(), rx.Component)
