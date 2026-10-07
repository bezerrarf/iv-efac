import pytest

def test_navigation_state_exists_and_switches():
    try:
        from projeto_web.state.navigation_state import NavigationState
    except ImportError:
        pytest.fail("NavigationState module not created yet.")
    
    state = NavigationState()
    assert state.tela_ativa == "inicio"
    assert state.indice_tela == 0
    
    state.proxima_tela()
    assert state.tela_ativa == "eixos"
    
    state.set_tela("sobre")
    assert state.tela_ativa == "sobre"
