import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import COLOR_BG, COLOR_SURFACE_GLASS, COLOR_BORDER_CYAN, STYLE_HEADING_RESPONSIVE, STYLE_TEXT_RESPONSIVE, STYLE_BUTTON_CHIP
from projeto_web.views.components.inscricao_sections.form_cadastro import form_cadastro
from projeto_web.views.components.inscricao_sections.form_login import form_login
from projeto_web.views.components.inscricao_sections.logged_in_hub import logged_in_hub

def inscricao_page() -> rx.Component:
    return rx.box(
        # Fundo Vetorial Cósmico Adaptativo
        cosmic_background(),

        navbar(),
        rx.box(
            rx.vstack(
                rx.badge("Portal de Credenciamento Oficial • IV EFAC", color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
                rx.heading(
                    "Inscrição & Credencial do Evento",
                    size=rx.breakpoints(initial="6", sm="7", md="8"),
                    weight="bold",
                    color="white",
                    text_align="center",
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(
                    "Cadastre-se gratuitamente para garantir sua vaga presencial no Campus Brejo Santo ou receber os links da transmissão online.",
                    size=rx.breakpoints(initial="2", sm="3"),
                    color="var(--gray-10)",
                    text_align="center",
                    max_width="660px",
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                rx.cond(
                    AuthState.is_logged_in,
                    logged_in_hub(),
                    rx.card(
                        rx.tabs.root(
                            rx.tabs.list(
                                rx.tabs.trigger("Nova Inscrição", value="cadastro"),
                                rx.tabs.trigger("Já sou Inscrito (Login)", value="login"),
                                size="2",
                            ),
                            rx.tabs.content(
                                form_cadastro(),
                                value="cadastro",
                                padding_top="1.5rem",
                            ),
                            rx.tabs.content(
                                form_login(),
                                value="login",
                                padding_top="1.5rem",
                            ),
                            default_value="cadastro",
                        ),
                        background=COLOR_SURFACE_GLASS,
                        backdrop_filter="blur(16px)",
                        border=f"1px solid {COLOR_BORDER_CYAN}",
                        border_radius="16px",
                        padding=rx.breakpoints(initial="1.25rem", sm="2rem"),
                        max_width="540px",
                        width="100%",
                        box_shadow="0 10px 40px rgba(0, 0, 0, 0.4)",
                    ),
                ),
                align="center",
                spacing="4",
                max_width="1100px",
                margin="0 auto",
                padding=rx.breakpoints(initial="2rem 1rem 4rem 1rem", sm="3rem 1.5rem 5rem 1.5rem"),
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
