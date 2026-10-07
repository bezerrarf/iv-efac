import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def tela_local() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.badge("Deslocamento & Credenciamento", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
            rx.heading("Localização & Inscrições", size=rx.breakpoints(initial="6", sm="7", md="8"), weight="bold", color="white", text_align="center", style=STYLE_HEADING_RESPONSIVE),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="map-pin", size=22, color=COLOR_CYAN),
                            rx.vstack(
                                rx.heading("Universidade Federal do Cariri (UFCA)", size="3", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                                rx.text("Instituto de Formação de Educadores – IFE • Campus Brejo Santo", size="2", color="var(--gray-11)", style=STYLE_TEXT_RESPONSIVE),
                                rx.text("Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE • CEP 63260-000", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        rx.divider(color_scheme="gray", opacity="0.15"),
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="plane", size=16, color=COLOR_CYAN),
                                rx.text("Aeroporto de Juazeiro do Norte (JDO) a ~65 km", size="1", style=STYLE_TEXT_RESPONSIVE),
                                spacing="1",
                            ),
                            rx.hstack(
                                rx.icon(tag="bus", size=16, color=COLOR_CYAN),
                                rx.text("Acesso pelas rodovias BR-116 e CE-397", size="1", style=STYLE_TEXT_RESPONSIVE),
                                spacing="1",
                            ),
                            spacing="3",
                            wrap="wrap",
                        ),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    width="100%",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                ),
                # Card de Inscrição Direta
                rx.card(
                    rx.vstack(
                        rx.heading("Garanta sua Vaga Gratuita no IV EFAC", size="4", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                        rx.text("Inscrição presencial no Campus Brejo Santo ou com acesso à transmissão global e certificação.", size="2", color="var(--gray-10)", style=STYLE_TEXT_RESPONSIVE),
                        rx.link(
                            rx.button(
                                "Fazer Inscrição Agora",
                                size="3",
                                radius="full",
                                padding_x="1.8rem",
                                background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                                color="white",
                                box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                                _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.55)"},
                                style=STYLE_BUTTON_CHIP,
                            ),
                            href="/inscricao",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    width="100%",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                max_width="1000px",
                width="100%",
            ),
            # Régua de Parceiros e Fomento
            rx.flex(
                parceiro_chip("FUNCAP", "Fomento Oficial"),
                parceiro_chip("Governo do Ceará", "Fomento Oficial"),
                parceiro_chip("UFCA / IFE", "Campus Brejo Santo"),
                parceiro_chip("ITA", "São José dos Campos"),
                parceiro_chip("CBPF", "Rio de Janeiro"),
                parceiro_chip("UFRGS", "Porto Alegre"),
                parceiro_chip("UFPB", "João Pessoa"),
                parceiro_chip("IFCE", "Ceará"),
                parceiro_chip("UECE", "Ceará"),
                parceiro_chip("URCA", "Cariri"),
                parceiro_chip("Observatório Kariri", "Divulgação"),
                gap="2",
                wrap="wrap",
                justify="center",
                max_width="920px",
                margin_top="0.8rem",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1rem",
        ),
        width="100%",
    )


