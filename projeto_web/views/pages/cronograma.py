"""Página de Cronograma oficial do IV EFAC (View).
Grade horária dos 2 dias oficiais (11 e 12 de Novembro de 2026).
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, Atividade


def timeline_card(item: Atividade) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.vstack(
                rx.badge(item.horario, color_scheme="cyan", variant="solid", size="2"),
                rx.text(item.local, size="1", color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)")),
                align="start",
                min_width=["80px", "110px"],
                spacing="1",
            ),
            rx.box(
                width="2px",
                height="100%",
                background=rx.color_mode_cond(light="#e2e8f0", dark="rgba(255, 255, 255, 0.1)"),
                margin_x="1rem",
                display=["none", "block"],
            ),
            rx.vstack(
                rx.hstack(
                    rx.badge(item.tipo, color_scheme=item.tipo_color, variant="soft", size="1"),
                    rx.spacer(),
                    align="center",
                    width="100%",
                ),
                rx.heading(
                    item.titulo,
                    size="4",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="white"),
                ),
                rx.text(
                    item.palestrante,
                    size="2",
                    weight="medium",
                    color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"),
                ),
                rx.text(
                    item.descricao,
                    size="2",
                    color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    line_height="1.5",
                ),
                spacing="1",
                align="start",
                width="100%",
            ),
            width="100%",
            align="start",
        ),
        background=rx.color_mode_cond(light="#ffffff", dark="rgba(15, 23, 42, 0.7)"),
        backdrop_filter="blur(10px)",
        border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.08)"),
        padding="1.25rem",
        margin_bottom="1rem",
        width="100%",
        box_shadow=rx.color_mode_cond(light="0 4px 15px rgba(0, 0, 0, 0.04)", dark="none"),
        _hover={"border_color": "rgba(0, 173, 181, 0.4)", "transform": "translateX(4px)"},
        transition="all 0.2s ease",
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
        navbar(),
        rx.box(
            rx.vstack(
                rx.badge("Programação Oficial • IV EFAC", color_scheme="cyan", variant="soft", size="2"),
                rx.heading(
                    "Grade Horária de Atividades",
                    size="8",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="white"),
                ),
                rx.text(
                    "Dois dias de imersão intensiva com conferências magnas, minicurso de Python, mesas-redondas e sessões de comunicação oral e pôsteres.",
                    size="3",
                    color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    text_align="center",
                    max_width="720px",
                ),
                # Seleção de Abas Dia 1 e Dia 2 com transição suave
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="calendar", size=16),
                            rx.text("Dia 1 • 11/Nov (Quarta-feira)", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        variant=rx.cond(EventoState.dia_selecionado == "Dia 1", "solid", "outline"),
                        color_scheme="indigo",
                        on_click=lambda: EventoState.set_dia("Dia 1"),
                        radius="full",
                        padding_x="1.6rem",
                        background=rx.cond(EventoState.dia_selecionado == "Dia 1", "#103460", "transparent"),
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="calendar", size=16),
                            rx.text("Dia 2 • 12/Nov (Quinta-feira)", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        variant=rx.cond(EventoState.dia_selecionado == "Dia 2", "solid", "outline"),
                        color_scheme="indigo",
                        on_click=lambda: EventoState.set_dia("Dia 2"),
                        radius="full",
                        padding_x="1.6rem",
                        background=rx.cond(EventoState.dia_selecionado == "Dia 2", "#103460", "transparent"),
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
                    max_width="900px",
                ),
                align="center",
                spacing="4",
                max_width="1150px",
                margin="0 auto",
                padding="3rem 1.5rem",
            ),
            width="100%",
        ),
        footer(),
        min_height="100vh",
        background=rx.color_mode_cond(light="#f8fafc", dark="#060814"),
        color=rx.color_mode_cond(light="#0f172a", dark="white"),
        transition="background 0.3s ease, color 0.3s ease",
    )
