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

def test_admin_state_excluir_atividade():
    assert hasattr(AdminState, "excluir_atividade")
    # Testa retorno antecipado silencioso para nao-admin
    dummy_unauth = types.SimpleNamespace(
        is_admin=False,
        feedback_msg="",
    )
    AdminState.excluir_atividade.fn(dummy_unauth, 999999)
    assert dummy_unauth.feedback_msg == ""

    # Testa execucao autorizada para admin com id invalido/inexistente
    dummy_auth = types.SimpleNamespace(
        is_admin=True,
        feedback_msg="",
        feedback_tipo="",
        is_editing_atividade=False,
        carregar_atividades_admin=lambda: None,
    )
    AdminState.excluir_atividade.fn(dummy_auth, 999999)
    # Se ID nao existe, ok e False e feedback_tipo e error
    assert dummy_auth.feedback_tipo == "error"

    # Testa criacao de EventSpec
    spec = AdminState.excluir_atividade(999999)
    assert spec is not None


def test_admin_state_links_modelos_oficiais():
    """Garante que os links oficiais dos modelos de submissao estao configurados por padrao."""
    fields = AdminState.get_fields()
    assert "1tp2I660zIwhE8SpjEmeSdNa4aGOx5TAN" in fields["link_modelo_resumo"].default
    assert "1iUEyNN3E_IglPo508DiXv8wOgi9emzqJ" in fields["link_modelo_slides"].default
    assert "1p12rVh3LbCWgHostLjOYgxG1Z0tpk1qc" in fields["link_modelo_poster"].default
