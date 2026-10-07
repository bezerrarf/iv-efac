import pytest

def test_supervisor_state_exists_and_isolates_logic():
    try:
        from projeto_web.state.supervisor_state import SupervisorState
    except ImportError:
        pytest.fail("SupervisorState module not created yet.")
    
    assert "superv_busca" in SupervisorState.vars
    assert "superv_inscritos" in SupervisorState.vars
    assert hasattr(SupervisorState, "carregar_painel_supervisor")
    assert hasattr(SupervisorState, "alternar_presenca_participante")
