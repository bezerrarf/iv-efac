import pytest
import reflex as rx

def test_inscricao_sections_are_components():
    try:
        from projeto_web.views.components.inscricao_sections.form_cadastro import form_cadastro
        from projeto_web.views.components.inscricao_sections.form_login import form_login
        from projeto_web.views.components.inscricao_sections.logged_in_hub import logged_in_hub
        from projeto_web.views.components.inscricao_sections.templates_pos_inscricao import templates_pos_inscricao
        from projeto_web.views.components.inscricao_sections.feedback_alert import feedback_alert
    except ImportError:
        pytest.fail("Não foi possível importar os módulos de seção. Certifique-se de que a refatoração ocorreu.")

    sections = [
        form_cadastro(),
        form_login(),
        logged_in_hub(),
        templates_pos_inscricao(),
        feedback_alert(),
    ]

    for section in sections:
        assert isinstance(section, rx.Component), f"A seção {section} não é um Componente Reflex."
