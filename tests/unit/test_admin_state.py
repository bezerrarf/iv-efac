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


def test_admin_state_excluir_participante_admin_seguranca():
    """Garante que excluir_participante_admin funciona sem AttributeError e restringe exclusivamente a admins."""
    # 1. Bloqueia não-admin (participante ou supervisor)
    dummy_nao_admin = types.SimpleNamespace(
        is_admin=False,
        user_role="supervisor",
        user_id=10,
        admin_edit_user_id=20,
        feedback_msg="",
        feedback_tipo="",
    )
    AdminState.excluir_participante_admin.fn(dummy_nao_admin)
    assert dummy_nao_admin.feedback_tipo == "error"
    assert "somente administradores" in dummy_nao_admin.feedback_msg

    # 2. Impede autoexclusão da própria conta de admin logada (sem usar self.current_user)
    dummy_self = types.SimpleNamespace(
        is_admin=True,
        user_role="admin",
        user_id=14,
        admin_edit_user_id=14,
        feedback_msg="",
        feedback_tipo="",
    )
    AdminState.excluir_participante_admin.fn(dummy_self)
    assert dummy_self.feedback_tipo == "error"
    assert "própria conta" in dummy_self.feedback_msg
