"""Testes unitários para a página de Normas de Submissão."""

from projeto_web.views.pages.normas_submissao import normas_submissao_page
import reflex as rx


def test_normas_submissao_render():
    """Garante que a página de normas de submissão instancia e renderiza sem erros."""
    component = normas_submissao_page()
    assert isinstance(component, rx.Component)
