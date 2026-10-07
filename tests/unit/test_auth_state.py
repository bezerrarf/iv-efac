import pytest

def test_auth_state_exists_and_isolates_auth_logic():
    try:
        from projeto_web.state.auth_state import AuthState
    except ImportError:
        pytest.fail("AuthState module not created yet.")
    
    # Check that variables exist in the Reflex class definition
    assert "is_logged_in" in AuthState.vars
    assert "user_nome" in AuthState.vars
    assert "cad_nome" in AuthState.vars
    assert "login_email" in AuthState.vars
    
    # Check methods exist on the class
    assert hasattr(AuthState, "realizar_login")
    assert hasattr(AuthState, "realizar_cadastro")
    assert hasattr(AuthState, "logout")
