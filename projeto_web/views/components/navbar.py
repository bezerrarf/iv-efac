"""Barra de Navegação Superior Oficial do IV EFAC.
Layout Solicitado:
- Esquerda: Marca/ícone anterior da Home (Logo oficial circular + texto IV EFAC 2026 • Física & Astronomia • UFCA).
- Centro: Ícone/badge anterior do Edital (Badge tracejada 'Edital' com pill 'Em Breve').
- Direita: Ícone único de acesso (login / perfil).
"""

import reflex as rx
from projeto_web.state.auth_state import AuthState
from projeto_web.views.components.modal_perfil import modal_meu_perfil
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_NAVBAR_BG,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_SUBTLE,
    STYLE_BUTTON_CHIP,
)


def nav_home_brand() -> rx.Component:
    """Marca oficial da Home: Logo circular com efeito cyan e tipografia acadêmica."""
    return rx.link(
        rx.hstack(
            rx.box(
                rx.image(
                    src="/logo_ivefac.jpeg",
                    alt="Logo Oficial IV EFAC 2026",
                    width="38px",
                    height="38px",
                    border_radius="50%",
                    object_fit="cover",
                    border="1.5px solid #00ADB5",
                    box_shadow="0 0 12px rgba(0, 173, 181, 0.5)",
                ),
                display="grid",
                place_items="center",
            ),
            rx.vstack(
                rx.hstack(
                    rx.heading(
                        "IV EFAC",
                        size="4",
                        weight="bold",
                        color="white",
                    ),
                    rx.badge("2026", color_scheme="cyan", variant="soft", size="1"),
                    spacing="1",
                    align="center",
                ),
                rx.text(
                    "Física & Astronomia • UFCA",
                    size="1",
                    color="#CBD5E1",
                    style={"white_space": "nowrap"},
                ),
                spacing="0",
                align="start",
            ),
            align="center",
            spacing="2",
        ),
        href="/#inicio",
        style=STYLE_BUTTON_CHIP,
        id="nav-brand-home",
    )


def nav_edital_em_breve() -> rx.Component:
    """Edital removido por solicitação."""
    return rx.fragment()


def navbar() -> rx.Component:
    """Barra superior com Home (esquerda), Edital Em Breve (centro) e Acesso (direita)."""
    nav_component = rx.box(
        rx.hstack(
            # CANTO ESQUERDO: Marca/Ícone Home anterior
            nav_home_brand(),

            

            # CANTO DIREITO (Oposto à Home): Ícone de acesso/login
            rx.hstack(
                rx.cond(
                    AuthState.is_logged_in,
                    # Usuário Autenticado
                    rx.hstack(
                        rx.link(
                            rx.tooltip(
                                rx.box(
                                    rx.hstack(
                                        rx.icon(tag="user-check", size=18, color=COLOR_CYAN),
                                        rx.text(
                                            AuthState.user_nome,
                                            size="1",
                                            weight="bold",
                                            color="white",
                                            max_width="120px",
                                            overflow="hidden",
                                            text_overflow="ellipsis",
                                            white_space="nowrap",
                                        ),
                                        spacing="1",
                                        align="center",
                                    ),
                                    padding="0.45rem 0.8rem",
                                    border_radius="10px",
                                    background="rgba(15, 23, 42, 0.85)",
                                    border=f"1.5px solid {COLOR_BORDER_CYAN}",
                                    _hover={
                                        "background": "rgba(0, 173, 181, 0.25)",
                                        "border_color": COLOR_CYAN,
                                        "transform": "scale(1.04)",
                                    },
                                    transition="all 0.2s ease",
                                    cursor="pointer",
                                    id="btn-nav-usuario-logado",
                                ),
                                content="Acessar Área do Participante / Painel",
                            ),
                            href="/inscricao",
                        ),
                        rx.tooltip(
                            rx.box(
                                rx.icon(tag="log-out", size=18, color="#F87171"),
                                padding="0.5rem",
                                border_radius="10px",
                                background="rgba(15, 23, 42, 0.8)",
                                border="1px solid rgba(248, 113, 113, 0.35)",
                                _hover={
                                    "background": "rgba(248, 113, 113, 0.2)",
                                    "border_color": "#F87171",
                                    "transform": "scale(1.06)",
                                },
                                transition="all 0.2s ease",
                                cursor="pointer",
                                on_click=AuthState.logout,
                                display="grid",
                                place_items="center",
                                id="btn-nav-logout",
                            ),
                            content="Encerrar Sessão",
                        ),
                        spacing="2",
                        align="center",
                    ),
                    # Visitante
                    rx.link(
                        rx.tooltip(
                            rx.box(
                                rx.icon(tag="log-in", size=22, color=COLOR_CYAN),
                                padding="0.55rem",
                                border_radius="12px",
                                background="rgba(15, 23, 42, 0.8)",
                                border=f"1.5px solid {COLOR_BORDER_CYAN}",
                                box_shadow="0 2px 10px rgba(0, 173, 181, 0.2)",
                                _hover={
                                    "background": "rgba(0, 173, 181, 0.25)",
                                    "border_color": COLOR_CYAN,
                                    "transform": "scale(1.08)",
                                    "box_shadow": "0 4px 18px rgba(0, 173, 181, 0.45)",
                                },
                                transition="all 0.2s ease",
                                display="grid",
                                place_items="center",
                                id="btn-nav-login",
                            ),
                            content="Acesso / Iniciar Sessão",
                        ),
                        href="/inscricao",
                    ),
                ),
                align="center",
            ),
            justify="between",
            align="center",
            max_width="1320px",
            margin="0 auto",
            padding="0.65rem 1.25rem",
            width="100%",
        ),
        position="sticky",
        top="0",
        z_index="100",
        backdrop_filter="blur(16px)",
        background=COLOR_NAVBAR_BG,
        border_bottom=f"1px solid {COLOR_BORDER_SUBTLE}",
        width="100%",
    )

    return rx.fragment(
        nav_component,
        modal_meu_perfil(),
    )
