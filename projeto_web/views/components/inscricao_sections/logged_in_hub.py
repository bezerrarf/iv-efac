import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

from projeto_web.views.components.badge_card import cartao_identificacao_digital
from projeto_web.views.components.painel_admin import painel_admin_view
from projeto_web.views.components.painel_supervisor import painel_supervisor_view
from .templates_pos_inscricao import templates_pos_inscricao
from .feedback_alert import feedback_alert

def logged_in_hub() -> rx.Component:
    """Hub interativo do participante, supervisor e administrador autenticado."""
    return rx.vstack(
        feedback_alert(),
        # Barra Superior de Status do Usuário
        rx.hstack(
            rx.hstack(
                rx.cond(
                    AuthState.user_foto_url != "",
                    rx.image(
                        src=AuthState.user_foto_url,
                        width="42px",
                        height="42px",
                        border_radius="50%",
                        object_fit="cover",
                        border="1.5px solid #00ADB5",
                    ),
                    rx.box(
                        rx.icon(tag="user", size=20, color=COLOR_CYAN),
                        background="rgba(0, 173, 181, 0.15)",
                        border_radius="50%",
                        padding="0.55rem",
                        display="grid",
                        place_items="center",
                    ),
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(AuthState.user_nome, size="3", weight="bold", color="white"),
                        rx.cond(
                            AuthState.is_admin,
                            rx.badge("ADMIN", color_scheme="red", variant="solid", size="1"),
                            rx.cond(
                                AuthState.is_supervisor,
                                rx.badge("SUPERVISOR(A)", color_scheme="violet", variant="solid", size="1"),
                                rx.badge("PARTICIPANTE", color_scheme="cyan", variant="solid", size="1"),
                            ),
                        ),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(
                        AuthState.user_email,
                        " • ",
                        AuthState.user_instituicao,
                        " (",
                        AuthState.user_modalidade,
                        ")",
                        size="1",
                        color="var(--gray-9)",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.spacer(),
            # Ação de Alterar Modalidade
            rx.hstack(
                rx.cond(
                    AuthState.user_modalidade == "Presencial",
                    rx.button(
                        "Mudar para Online",
                        size="1",
                        variant="outline",
                        color_scheme="cyan",
                        on_click=EventoState.alterar_modalidade_usuario("Online"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.button(
                        "Mudar para Presencial",
                        size="1",
                        variant="outline",
                        color_scheme="indigo",
                        on_click=EventoState.alterar_modalidade_usuario("Presencial"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                ),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="log-out", size=14),
                        rx.text("Sair", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    variant="ghost",
                    color_scheme="red",
                    size="2",
                    on_click=AuthState.logout,
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="2",
                align="center",
            ),
            width="100%",
            align="center",
            padding="1rem 1.25rem",
            background="rgba(15, 23, 42, 0.85)",
            border="1px solid rgba(0, 173, 181, 0.25)",
            border_radius="14px",
            box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
            wrap="wrap",
            gap="2",
        ),
        # Navegação em Abas do Hub
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger(
                    rx.hstack(
                        rx.icon(tag="contact", size=15),
                        rx.text("Cartão de Identificação (Crachá)", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    value="cracha",
                ),
                rx.cond(
                    AuthState.is_admin,
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="shield-alert", size=15),
                            rx.text("Painel do Administrador", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="admin",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    AuthState.is_supervisor,
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="clipboard-check", size=15),
                            rx.text("Conferência de Presença", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="presenca",
                    ),
                    rx.fragment(),
                ),
                rx.tabs.trigger(
                    rx.hstack(
                        rx.icon(tag="file-down", size=15),
                        rx.text("Modelos & Submissões", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    value="modelos",
                ),
                size="2",
            ),
            rx.tabs.content(
                cartao_identificacao_digital(),
                value="cracha",
                padding_top="1.5rem",
                width="100%",
            ),
            rx.tabs.content(
                painel_admin_view(),
                value="admin",
                padding_top="1.5rem",
                width="100%",
            ),
            rx.tabs.content(
                painel_supervisor_view(),
                value="presenca",
                padding_top="1.5rem",
                width="100%",
            ),
            rx.tabs.content(
                templates_pos_inscricao(),
                value="modelos",
                padding_top="1.5rem",
                width="100%",
            ),
            default_value="cracha",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="920px",
    )


