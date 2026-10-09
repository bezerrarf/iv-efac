import pytest
import types
from unittest.mock import MagicMock, patch
from projeto_web.state.auth_state import AuthState
from projeto_web.models.usuario import Usuario

def test_auth_state_exists_and_isolates_auth_logic():
    # Check that variables exist in the Reflex class definition
    assert "is_logged_in" in AuthState.vars
    assert "user_nome" in AuthState.vars
    assert "cad_nome" in AuthState.vars
    assert "login_email" in AuthState.vars
    
    # Check methods exist on the class
    assert hasattr(AuthState, "realizar_login")
    assert hasattr(AuthState, "realizar_cadastro")
    assert hasattr(AuthState, "logout")

def test_auth_state_realizar_login_admin_does_not_raise_attribute_error():
    """Garante que o login de administrador autentica sem tentar invocar métodos inexistentes em AuthState."""
    dummy = types.SimpleNamespace(
        login_email="admin@ufca.edu.br",
        login_senha="Admin_IVEFAC_2026!",
        feedback_msg="",
        feedback_tipo="",
        is_logged_in=False,
        user_id=0,
        user_nome="",
        user_email="",
        user_instituicao="",
        user_modalidade="",
        user_area="",
        user_codigo="",
        user_role="",
        user_foto_url="",
        user_presenca=False,
        usuario_logado_email_confirmado=False,
        email_confirmado=False,
        is_admin=False,
        is_supervisor=False,
        limpar_feedback=lambda: None,
    )
    mock_usuario = Usuario(
        id=1,
        nome="Coordenação Geral IV EFAC",
        email="admin@ufca.edu.br",
        instituicao="Universidade Federal do Cariri (UFCA)",
        modalidade="Presencial",
        area="Comissão Organizadora",
        senha_hash="dummy_hash",
        codigo_inscricao="ADMIN-001",
        role="admin",
        presenca_confirmada=False,
        email_confirmado=True,
    )
    mock_ctrl = MagicMock()
    mock_ctrl.autenticar.return_value = types.SimpleNamespace(sucesso=True, dado=mock_usuario, mensagem="")
    with patch("projeto_web.state.auth_state._usuario_controller", mock_ctrl):
        fn = getattr(AuthState.realizar_login, "fn", AuthState.realizar_login)
        fn(dummy)
        assert dummy.is_logged_in is True
        assert dummy.is_admin is True
        assert dummy.feedback_tipo == "success"
