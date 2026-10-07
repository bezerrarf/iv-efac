import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_submissoes() -> rx.Component:
    normas = EventoController.obter_normas_submissao()

    return rx.box(
        rx.vstack(
            rx.badge("Publicação Oficial nos Anais", color_scheme="indigo", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading("Chamada de Trabalhos (Submissões)", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color="white", text_align="center", style=STYLE_HEADING_RESPONSIVE),
            rx.text(
                "Submeta seu resumo expandido para publicação nos Anais oficiais do IV EFAC.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="var(--gray-10)",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Diretrizes de Envio", size="3", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                        rx.divider(color_scheme="gray", opacity="0.15"),
                        rx.text(f"• Formato: {normas.formato}", size="2", style=STYLE_TEXT_RESPONSIVE),
                        rx.text(f"• Extensão: {normas.paginas}", size="2", style=STYLE_TEXT_RESPONSIVE),
                        rx.text(f"• Modalidades: {normas.modalidade}", size="2", style=STYLE_TEXT_RESPONSIVE),
                        rx.text(f"• Publicação: {normas.publicacao}", size="2", style=STYLE_TEXT_RESPONSIVE),
                        spacing="2",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Critérios da Comissão", size="3", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                        rx.divider(color_scheme="gray", opacity="0.15"),
                        *[
                            rx.hstack(
                                rx.icon(tag="circle-check", size=16, color="#059669"),
                                rx.text(crit, size="2", style=STYLE_TEXT_RESPONSIVE),
                                spacing="2",
                                align="center",
                            )
                            for crit in normas.criterios
                        ],
                        spacing="1",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                max_width="920px",
                width="100%",
                margin_top="0.8rem",
            ),
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon(tag="upload", size=16),
                        rx.text("Acessar Área do Participante para Submeter"),
                        spacing="2",
                        align="center",
                    ),
                    size="3",
                    radius="full",
                    padding_x="2rem",
                    font_weight="bold",
                    background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                    color="white",
                    box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                    _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.55)"},
                    style=STYLE_BUTTON_CHIP,
                ),
                href="/inscricao",
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


# --- 7. TELA LOCAL & INSCRIÇÃO: COORDENADAS & CREDENCIAIS ---

