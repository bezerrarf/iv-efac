import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.state.navigation_state import NavigationState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_palestrantes() -> rx.Component:
    palestrantes = EventoController.obter_palestrantes()

    def keynote_card_hpc(p: Palestrante) -> rx.Component:
        return rx.card(
            rx.vstack(
                rx.avatar(
                    fallback=p.nome[6:8].upper() if len(p.nome) > 8 else p.nome[:2].upper(),
                    size="4",
                    radius="full",
                    color_scheme="cyan",
                ),
                rx.heading(p.nome, size="3", weight="bold", text_align="center", color="white", style=STYLE_HEADING_RESPONSIVE),
                rx.text(p.cargo, size="1", color=COLOR_CYAN_LIGHT, text_align="center", style=STYLE_TEXT_RESPONSIVE),
                rx.badge(p.instituicao, size="1", variant="soft", color_scheme="indigo", style=STYLE_BUTTON_CHIP),
                rx.text(
                    p.especialidade,
                    size="1",
                    color="var(--gray-10)",
                    text_align="center",
                    line_height="1.45",
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                spacing="1",
                align="center",
            ),
            padding="1.2rem",
            width="100%",
            border_radius="14px",
            background=COLOR_SURFACE_GLASS,
            backdrop_filter="blur(16px)",
            border=f"1px solid {COLOR_BORDER_CYAN}",
            box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
            _hover={"transform": "translateY(-3px)", "border_color": COLOR_CYAN, "box_shadow": "0 10px 32px rgba(0, 173, 181, 0.2)"},
            transition="all 0.2s ease",
        )

    return rx.box(
        rx.vstack(
            rx.badge("Quadro Técnico Internacional & Nacional", color_scheme="indigo", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading("Palestrantes Convidados (Keynotes)", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color="white", text_align="center", style=STYLE_HEADING_RESPONSIVE),
            rx.text(
                "Pesquisadores líderes do ITA (São José dos Campos), CBPF, UFRGS, UFPB, IFCE e UECE.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="var(--gray-10)",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.grid(
                *[keynote_card_hpc(p) for p in palestrantes],
                columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                spacing="3",
                max_width="1220px",
                width="100%",
                margin_top="1rem",
            ),
            rx.button(
                rx.hstack(
                    rx.text("Conferir a Grade Horária"),
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
                on_click=NavigationState.set_tela("programacao"),
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


# --- 5. TELA PROGRAMAÇÃO: TERMINAL DE GRADE ---

