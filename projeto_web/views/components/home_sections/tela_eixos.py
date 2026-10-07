import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_eixos() -> rx.Component:
    eixos = EventoController.obter_eixos_tematicos()

    def card_eixo_hpc(e: EixoTematico) -> rx.Component:
        return rx.card(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag=e.icone, size=22, color=e.cor),
                        padding="0.6rem",
                        border_radius="12px",
                        background=f"{e.cor}18",
                    ),
                    rx.badge(f"Eixo {e.numero}", color_scheme="cyan", variant="surface", size="2", style=STYLE_BUTTON_CHIP),
                    spacing="2",
                    align="center",
                ),
                rx.heading(e.titulo, size="4", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                rx.text(e.subtitulo, size="2", weight="medium", color=COLOR_CYAN_LIGHT, style=STYLE_HEADING_RESPONSIVE),
                rx.text(e.descricao, size="2", color="var(--gray-10)", line_height="1.55", style=STYLE_TEXT_RESPONSIVE),
                rx.divider(color_scheme="gray", opacity="0.15"),
                rx.hstack(
                    *[rx.badge(t, size="1", variant="outline", style=STYLE_BUTTON_CHIP) for t in e.tags],
                    spacing="1",
                    wrap="wrap",
                ),
                spacing="3",
                align="start",
            ),
            padding="1.5rem",
            border_radius="16px",
            height="100%",
            background=COLOR_SURFACE_GLASS,
            backdrop_filter="blur(16px)",
            border=f"1px solid {COLOR_BORDER_CYAN}",
            box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
            _hover={"transform": "translateY(-4px)", "border_color": e.cor, "box_shadow": f"0 12px 35px {e.cor}25"},
            transition="all 0.22s ease",
        )

    return rx.box(
        rx.vstack(
            rx.badge("Matriz Interdisciplinar", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading("Eixos Temáticos do Encontro", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color="white", text_align="center", style=STYLE_HEADING_RESPONSIVE),
            rx.text(
                "Estrutura temática para apresentação de artigos, resumos expandidos e mesas de debate.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="var(--gray-10)",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.grid(
                *[card_eixo_hpc(e) for e in eixos],
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                spacing="4",
                max_width="1240px",
                width="100%",
                margin_top="1rem",
            ),
            rx.button(
                rx.hstack(
                    rx.text("Conhecer os Palestrantes Destas Áreas"),
                    rx.icon(tag="arrow-right", size=16),
                    spacing="1",
                    align="center",
                ),
                size="3",
                radius="full",
                background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                color="white",
                box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                margin_top="1.5rem",
                on_click=EventoState.set_tela("palestrantes"),
                style=STYLE_BUTTON_CHIP,
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


# --- 4. TELA PALESTRANTES: KEYNOTES SUMMIT ---

