"""Página de Cronograma oficial do IV EFAC (View - UI/UX Pro Max).
Grade horária dos 2 dias oficiais (11 e 12 de Novembro de 2026).
Pure Deep Cosmic Dark Theme com responsividade completa para todas as telas.
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, Atividade
from projeto_web.styles.theme import (
    COLOR_BG,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_SUBTLE,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
    STYLE_BUTTON_CHIP,
)


def timeline_card(item: Atividade) -> rx.Component:
    """Card de atividade da programação com micro-efeito e adaptação total de tela."""
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.badge(item.horario, color_scheme="cyan", variant="solid", size="2", style=STYLE_BUTTON_CHIP),
                rx.text(item.local, size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                align="start",
                min_width=["80px", "110px"],
                spacing="1",
            ),
            rx.box(
                width="2px",
                height="100%",
                background="rgba(0, 173, 181, 0.25)",
                margin_x=["0.5rem", "1rem"],
                display=["none", "block"],
            ),
            rx.vstack(
                rx.hstack(
                    rx.badge(item.tipo, color_scheme=item.tipo_color, variant="soft", size="1", style=STYLE_BUTTON_CHIP),
                    rx.spacer(),
                    align="center",
                    width="100%",
                ),
                rx.heading(
                    item.titulo,
                    size=rx.breakpoints(initial="3", sm="4"),
                    weight="bold",
                    color="white",
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(
                    item.palestrante,
                    size="2",
                    weight="medium",
                    color=COLOR_CYAN_LIGHT,
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                rx.text(
                    item.descricao,
                    size="2",
                    color="var(--gray-10)",
                    line_height="1.55",
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                spacing="1",
                align="start",
                width="100%",
            ),
            width="100%",
            align="start",
            spacing="3",
        ),
        background=COLOR_SURFACE_GLASS,
        backdrop_filter="blur(16px)",
        border=f"1px solid {COLOR_BORDER_CYAN}",
        border_radius="14px",
        padding=rx.breakpoints(initial="1rem", sm="1.25rem"),
        margin_bottom="1rem",
        width="100%",
        box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
        _hover={
            "border_color": "rgba(0, 173, 181, 0.6)",
            "transform": "translateX(4px)",
            "box_shadow": "0 10px 35px rgba(0, 173, 181, 0.15)",
        },
        transition="all 0.22s ease",
    )


def dia_content(dia_nome: str) -> rx.Component:
    atividades = EventoController.obter_programacao(dia_nome)
    return rx.vstack(
        *[timeline_card(item) for item in atividades],
        width="100%",
        spacing="2",
    )


def cronograma_page() -> rx.Component:
    return rx.box(
        # Fundo Vetorial Cósmico Adaptativo
        cosmic_background(),

        navbar(),
        rx.box(
            rx.vstack(
                rx.badge("Programação Oficial • IV EFAC", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
                rx.heading(
                    "Grade Horária de Atividades",
                    size=rx.breakpoints(initial="6", sm="7", md="8"),
                    weight="bold",
                    color="white",
                    text_align="center",
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(
                    "Dois dias de imersão intensiva com conferências magnas, minicurso de Python, mesas-redondas e sessões de comunicação oral e pôsteres.",
                    size=rx.breakpoints(initial="2", sm="3"),
                    color="var(--gray-10)",
                    text_align="center",
                    max_width="740px",
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                # Seleção de Abas Dia 1 e Dia 2 com transição cósmica
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="calendar", size=16),
                            rx.text("Dia 1 • 11/Nov (Quarta-feira)", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        variant=rx.cond(EventoState.dia_selecionado == "Dia 1", "solid", "outline"),
                        color_scheme="cyan",
                        on_click=lambda: EventoState.set_dia("Dia 1"),
                        radius="full",
                        padding_x="1.6rem",
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
                        box_shadow=rx.cond(
                            EventoState.dia_selecionado == "Dia 1",
                            "0 4px 18px rgba(0, 173, 181, 0.4)",
                            "none",
                        ),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="calendar", size=16),
                            rx.text("Dia 2 • 12/Nov (Quinta-feira)", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        variant=rx.cond(EventoState.dia_selecionado == "Dia 2", "solid", "outline"),
                        color_scheme="cyan",
                        on_click=lambda: EventoState.set_dia("Dia 2"),
                        radius="full",
                        padding_x="1.6rem",
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
                        box_shadow=rx.cond(
                            EventoState.dia_selecionado == "Dia 2",
                            "0 4px 18px rgba(0, 173, 181, 0.4)",
                            "none",
                        ),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    spacing="3",
                    margin_y="1.5rem",
                    wrap="wrap",
                    justify="center",
                ),
                rx.box(
                    rx.cond(
                        EventoState.dia_selecionado == "Dia 1",
                        dia_content("Dia 1"),
                        dia_content("Dia 2"),
                    ),
                    width="100%",
                    max_width="920px",
                ),
                align="center",
                spacing="4",
                max_width="1150px",
                margin="0 auto",
                padding=rx.breakpoints(initial="2rem 1rem", sm="3rem 1.5rem"),
            ),
            width="100%",
            position="relative",
            z_index="2",
        ),
        footer(),
        min_height="100vh",
        background=COLOR_BG,
        color="white",
        position="relative",
    )
