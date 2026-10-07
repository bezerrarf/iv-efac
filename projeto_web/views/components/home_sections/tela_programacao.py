import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_programacao() -> rx.Component:
    dia1 = EventoController.obter_programacao("Dia 1")
    dia2 = EventoController.obter_programacao("Dia 2")

    def schedule_item_hpc(item: Atividade) -> rx.Component:
        return rx.card(
            rx.hstack(
                rx.badge(item.horario, color_scheme="cyan", variant="solid", size="1", style=STYLE_BUTTON_CHIP),
                rx.vstack(
                    rx.hstack(
                        rx.badge(item.tipo, color_scheme=item.tipo_color, size="1", variant="soft", style=STYLE_BUTTON_CHIP),
                        rx.text(item.local, size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(item.titulo, size="2", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
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

    return rx.box(
        rx.vstack(
            rx.badge("Grade Oficial • 2 Dias", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading("Programação do Simpósio", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color="white", text_align="center", style=STYLE_HEADING_RESPONSIVE),
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
            rx.box(
                rx.cond(
                    EventoState.dia_selecionado == "Dia 1",
                    rx.vstack(*[schedule_item_hpc(item) for item in dia1]),
                    rx.vstack(*[schedule_item_hpc(item) for item in dia2]),
                ),
                width="100%",
                max_width="860px",
                max_height="420px",
                overflow_y="auto",
            ),
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
                rx.button(
                    rx.hstack(
                        rx.text("Ver Regras de Submissão"),
                        rx.icon(tag="arrow-right", size=15),
                        spacing="1",
                        align="center",
                    ),
                    size="2",
                    radius="full",
                    background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                    color="white",
                    box_shadow="0 4px 16px rgba(0, 173, 181, 0.35)",
                    on_click=EventoState.set_tela("submissoes"),
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="3",
                margin_top="0.8rem",
                wrap="wrap",
                justify="center",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        width="100%",
    )


# --- 6. TELA SUBMISSÕES: CALL FOR PAPERS ---

