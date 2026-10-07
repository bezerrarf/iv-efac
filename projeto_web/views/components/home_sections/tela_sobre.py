import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_sobre() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.badge("Origens & Cooperação Internacional", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading(
                "Sobre o Encontro & Consolidação Regional",
                size=rx.breakpoints(initial="6", sm="7", md="8"),
                weight="bold",
                color="white",
                text_align="center",
                style=STYLE_HEADING_RESPONSIVE,
            ),
            rx.text(
                "Desde 2019, o EFAC é a principal plataforma de integração entre a pesquisa "
                "de ponta em física relativística e a formação de cientistas e educadores no interior cearense.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="var(--gray-10)",
                text_align="center",
                max_width="760px",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.grid(
                # Card Radiotelescópio BINGO
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="radio", size=24, color=COLOR_CYAN),
                            rx.heading("Acordo UFCA-USP & Radiotelescópio BINGO", size="4", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "O pioneirismo do encontro nasceu associado à colaboração científica no "
                            "projeto do Radiotelescópio BINGO (Baryon Acoustic Oscillations in Neutral Gas Observations), "
                            "conectando o Cariri à cosmologia observacional de classe mundial.",
                            size="2",
                            color="var(--gray-11)",
                            line_height="1.6",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.6rem",
                    border_radius="16px",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.35)",
                ),
                # Card Fomento Oficial FUNCAP
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="award", size=24, color=COLOR_CYAN),
                            rx.heading("Fomento Oficial FUNCAP • Governo do Ceará", size="4", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "Financiado com Fomento FUNCAP de Apoio a Eventos Científicos "
                            "(Processo: CER-0264-00190.01.00/26), o IV EFAC viabiliza a interiorização "
                            "efetiva da pós-graduação e iniciação científica no IFE – Campus Brejo Santo.",
                            size="2",
                            color="var(--gray-11)",
                            line_height="1.6",
                            style=STYLE_TEXT_RESPONSIVE,
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.6rem",
                    border_radius="16px",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 32px rgba(0, 0, 0, 0.35)",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="5",
                max_width="1060px",
                width="100%",
                margin_top="1rem",
            ),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.text("Explorar os 4 Eixos Temáticos"),
                        rx.icon(tag="arrow-right", size=16),
                        spacing="1",
                        align="center",
                    ),
                    size="3",
                    radius="full",
                    background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                    color="white",
                    box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                    on_click=EventoState.set_tela("eixos"),
                    style=STYLE_BUTTON_CHIP,
                ),
                margin_top="1.5rem",
            ),
            spacing="4",
            align="center",
            justify="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_y="2rem",
        ),
        width="100%",
    )


# --- 3. TELA EIXOS: MATRIZ DE PESQUISA HPC ---

