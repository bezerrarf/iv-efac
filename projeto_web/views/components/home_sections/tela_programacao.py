"""Seção de Programação do Simpósio reestruturada para a Landing Page única (UI/UX Pro Max).
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, Atividade
from projeto_web.styles.theme import (
    COLOR_TEXT_PRIMARY,

    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    STYLE_BUTTON_CHIP,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)


def _schedule_item_landing(item: Atividade) -> rx.Component:
    """Card individual de atividade para a grade na Landing Page."""
    return rx.card(
        rx.hstack(
            rx.badge(item.horario, color_scheme="cyan", variant="solid", size="1", style=STYLE_BUTTON_CHIP),
            rx.vstack(
                rx.hstack(
                    rx.badge(item.tipo, color_scheme=item.tipo_color, size="1", variant="soft", style=STYLE_BUTTON_CHIP),
                    rx.text(item.local, size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(item.titulo, size="2", weight="bold", color=COLOR_TEXT_PRIMARY, style=STYLE_HEADING_RESPONSIVE),
                rx.text(item.palestrante, size="1", color=COLOR_CYAN_LIGHT, style=STYLE_TEXT_RESPONSIVE),
                spacing="0",
                align="start",
                width="100%",
            ),
            align="start",
            spacing="3",
            width="100%",
        ),
        padding="0.85rem",
        width="100%",
        margin_bottom="0.4rem",
        border_radius="12px",
        background=COLOR_SURFACE_GLASS,
        backdrop_filter="blur(16px)",
        border=f"1px solid {COLOR_BORDER_CYAN}",
    )


def tela_programacao() -> rx.Component:
    """Seção de Grade Horária do Simpósio adaptada para o fluxo contínuo da Landing Page."""
    dia1 = EventoController.obter_programacao("Dia 1")
    dia2 = EventoController.obter_programacao("Dia 2")

    return rx.box(
        rx.vstack(
            rx.heading("Programação do Simpósio", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color=COLOR_TEXT_PRIMARY, text_align="center", style=STYLE_HEADING_RESPONSIVE),
            rx.text(
                "Dois dias de imersão acadêmica com conferências magnas, palestras convidadas e sessões temáticas.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="#E2E8F0",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            # Alternância de Dias
            rx.hstack(
                rx.button(
                    "Dia 1 • 11/Nov (Quarta-feira)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 1", "solid", "outline"),
                    color_scheme="cyan",
                    on_click=EventoState.set_dia("Dia 1"),
                    radius="full",
                    size="2",
                    padding_x="1.4rem",
                    background=rx.cond(
                        EventoState.dia_selecionado == "Dia 1",
                        "linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                        "transparent",
                    ),
                    border=rx.cond(
                        EventoState.dia_selecionado == "Dia 1",
                        "none",
                        f"1px solid {COLOR_BORDER_CYAN}",
                    ),
                    style=STYLE_BUTTON_CHIP,
                ),
                rx.button(
                    "Dia 2 • 12/Nov (Quinta-feira)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 2", "solid", "outline"),
                    color_scheme="cyan",
                    on_click=EventoState.set_dia("Dia 2"),
                    radius="full",
                    size="2",
                    padding_x="1.4rem",
                    background=rx.cond(
                        EventoState.dia_selecionado == "Dia 2",
                        "linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                        "transparent",
                    ),
                    border=rx.cond(
                        EventoState.dia_selecionado == "Dia 2",
                        "none",
                        f"1px solid {COLOR_BORDER_CYAN}",
                    ),
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="3",
                wrap="wrap",
                justify="center",
            ),
            # Lista de Itens com Scroll Suave
            rx.box(
                rx.cond(
                    EventoState.dia_selecionado == "Dia 1",
                    rx.vstack(*[_schedule_item_landing(item) for item in dia1], width="100%"),
                    rx.vstack(*[_schedule_item_landing(item) for item in dia2], width="100%"),
                ),
                width="100%",
                max_width="880px",
                max_height="460px",
                overflow_y="auto",
                padding_right="0.5rem",
            ),
            # Botões de Ação
            rx.hstack(
                rx.link(
                    rx.button(
                        "Abrir Grade Expandida Completa",
                        variant="outline",
                        color_scheme="cyan",
                        size="2",
                        radius="full",
                        border=f"1.5px solid {COLOR_BORDER_CYAN}",
                        color=COLOR_CYAN,
                        _hover={"background": "rgba(0, 173, 181, 0.15)"},
                        style=STYLE_BUTTON_CHIP,
                    ),
                    href="/cronograma",
                ),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.text("Garantir Inscrição Gratuita"),
                            rx.icon(tag="arrow-right", size=15),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        radius="full",
                        background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                        color=COLOR_TEXT_PRIMARY,
                        box_shadow="0 4px 16px rgba(0, 173, 181, 0.35)",
                        style=STYLE_BUTTON_CHIP,
                    ),
                    href="/inscricao",
                ),
                spacing="3",
                margin_top="1rem",
                wrap="wrap",
                justify="center",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="2rem",
        ),
        width="100%",
        id="programacao",
    )
