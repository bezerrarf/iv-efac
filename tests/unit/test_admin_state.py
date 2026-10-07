import pytest

def test_admin_state_exists_and_isolates_logic():
    try:
        from projeto_web.state.admin_state import AdminState
    except ImportError:
        pytest.fail("AdminState module not created yet.")
    
    # Verifica se as variáveis de painel e atividades existem na classe
    assert "admin_filtro_busca" in AdminState.vars
    assert "admin_inscritos" in AdminState.vars
    assert "admin_atividades" in AdminState.vars
    assert "is_creating_atividade" in AdminState.vars
    
    # Verifica se os métodos principais foram extraídos
    assert hasattr(AdminState, "carregar_painel_admin")
    assert hasattr(AdminState, "criar_nova_atividade")
    assert hasattr(AdminState, "exportar_inscritos_pdf")
