import pytest
import types
from projeto_web.state.supervisor_state import SupervisorState

def test_supervisor_state_exists_and_isolates_logic():
    # Verifica variáveis de busca e contadores
    assert "superv_busca" in SupervisorState.vars
    assert "superv_inscritos" in SupervisorState.vars
    assert "superv_presentes_count" in SupervisorState.vars
    assert "superv_total_count" in SupervisorState.vars
    
    # Verifica métodos
    assert hasattr(SupervisorState, "set_superv_busca")
    assert hasattr(SupervisorState, "carregar_painel_supervisor")
    assert hasattr(SupervisorState, "alternar_presenca_participante")

def test_supervisor_state_carregar_painel_executes_without_errors():
    """Garante que carregar_painel_supervisor executa sem NameError ou ausência de controller."""
    dummy = types.SimpleNamespace(
        superv_busca="",
        superv_inscritos=[],
        superv_total_count=0,
        superv_presentes_count=0,
    )
    SupervisorState.carregar_painel_supervisor(dummy)
    assert isinstance(dummy.superv_inscritos, list)
    assert dummy.superv_total_count >= 0
