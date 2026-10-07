import pytest
import reflex as rx

def test_home_sections_are_components():
    try:
        from projeto_web.views.components.home_sections.tela_inicio import tela_inicio
        from projeto_web.views.components.home_sections.tela_eixos import tela_eixos
        from projeto_web.views.components.home_sections.tela_palestrantes import tela_palestrantes
        from projeto_web.views.components.home_sections.tela_programacao import tela_programacao
        from projeto_web.views.components.home_sections.tela_submissoes import tela_submissoes
        from projeto_web.views.components.home_sections.tela_local import tela_local
        from projeto_web.views.components.home_sections.tela_sobre import tela_sobre
    except ImportError:
        pytest.fail("Não foi possível importar os módulos de seção. Certifique-se de que a refatoração ocorreu.")

    sections = [
        tela_inicio(),
        tela_eixos(),
        tela_palestrantes(),
        tela_programacao(),
        tela_submissoes(),
        tela_local(),
        tela_sobre(),
    ]

    for section in sections:
        assert isinstance(section, rx.Component), f"A seção {section} não é um Componente Reflex."
