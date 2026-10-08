import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.state.evento_state import EventoState
from projeto_web.state.navigation_state import NavigationState
from projeto_web.styles.theme import COLOR_BG, COLOR_NAVBAR_BG, COLOR_BORDER_CYAN, COLOR_BORDER_SUBTLE, STYLE_TEXT_RESPONSIVE
from projeto_web.views.components.home_sections.tela_inicio import tela_inicio
from projeto_web.views.components.home_sections.tela_sobre import tela_sobre
from projeto_web.views.components.home_sections.tela_eixos import tela_eixos
from projeto_web.views.components.home_sections.tela_palestrantes import tela_palestrantes
from projeto_web.views.components.home_sections.tela_programacao import tela_programacao
from projeto_web.views.components.home_sections.tela_submissoes import tela_submissoes
from projeto_web.views.components.home_sections.tela_local import tela_local

def home_page() -> rx.Component:
    return rx.box(
        # Fundo Vetorial Cósmico Adaptativo
        cosmic_background(),

        # Topo com navegação integrada de seções
        navbar(),

        # Palco Central de Tela Única
        rx.box(
            rx.cond(
                NavigationState.tela_ativa == "inicio",
                tela_inicio(),
                rx.cond(
                    NavigationState.tela_ativa == "eixos",
                    tela_eixos(),
                    rx.cond(
                        NavigationState.tela_ativa == "palestrantes",
                        tela_palestrantes(),
                        rx.cond(
                            NavigationState.tela_ativa == "programacao",
                            tela_programacao(),
                            rx.cond(
                                NavigationState.tela_ativa == "submissoes",
                                tela_submissoes(),
                                rx.cond(
                                    NavigationState.tela_ativa == "local",
                                    tela_local(),
                                    tela_sobre(),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            width="100%",
            max_width="1320px",
            margin="0 auto",
            padding_x=rx.breakpoints(initial="1rem", sm="1.5rem"),
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="calc(100vh - 120px)",
            position="relative",
            z_index="2",
        ),

        # Rodapé Mínimo Discreto
        rx.box(
            rx.text(
                "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Desenvolvido por Ramon Firmino Bezerra.",
                size="1",
                color="var(--gray-8)",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            padding_y="0.6rem",
            border_top=f"1px solid {COLOR_BORDER_SUBTLE}",
            background=COLOR_NAVBAR_BG,
            backdrop_filter="blur(10px)",
            width="100%",
            position="relative",
            z_index="2",
        ),

        min_height="100vh",
        background=COLOR_BG,
        color="white",
        position="relative",
        overflow="hidden",
    )
