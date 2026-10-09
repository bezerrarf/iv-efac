import pytest
import types
from projeto_web.state.admin_state import AdminState

def test_admin_state_exists_and_isolates_logic():
    # Verifica se as variáveis de painel e atividades existem na classe
    assert "admin_filtro_busca" in AdminState.vars
    assert "admin_inscritos" in AdminState.vars
    assert "admin_atividades" in AdminState.vars
    assert "is_creating_atividade" in AdminState.vars
    
    # Verifica se os métodos principais foram extraídos
    assert hasattr(AdminState, "carregar_painel_admin")
    assert hasattr(AdminState, "criar_nova_atividade")
    assert hasattr(AdminState, "exportar_inscritos_pdf")

def test_admin_state_carregar_painel_executes_without_errors():
    """Garante que carregar_painel_admin e carregar_atividades_admin não sofrem de NameError ou falta de controller."""
    dummy = types.SimpleNamespace(
        admin_filtro_busca="",
        admin_inscritos=[],
        admin_atividades=[],
        admin_total_inscritos=0,
        admin_total_presenciais=0,
        admin_total_onlines=0,
        admin_total_presentes=0,
        admin_total_supervisores=0,
    )
    # Testa a execução do método desvinculado de proxy reflex
    AdminState.carregar_atividades_admin(dummy)
    assert isinstance(dummy.admin_atividades, list)

    AdminState.carregar_painel_admin(dummy)
    assert isinstance(dummy.admin_inscritos, list)
    assert dummy.admin_total_inscritos >= 0
