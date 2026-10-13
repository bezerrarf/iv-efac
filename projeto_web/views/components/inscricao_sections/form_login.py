import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

from .feedback_alert import feedback_alert


def card_recuperacao_senha() -> rx.Component:
    """Card institucional acolhedor e profissional para solicitação de redefinição de senha ao Prof. Dr. Edson Otoniel."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon(tag="key-round", size=18, color="#38bdf8"),
                    rx.heading("Redefinição de Senha de Acesso", size="2", weight="bold", color="white"),
                    spacing="2",
                    align="center",
                ),
                rx.spacer(),
                rx.icon(
                    tag="x",
                    size=16,
                    color="#CBD5E1",
                    _hover={"color": "white"},
                    cursor="pointer",
                    on_click=AuthState.fechar_aviso_recuperacao_senha,
                ),
                width="100%",
                align="center",
            ),
            rx.text(
                "Por diretrizes de segurança institucional, a redefinição de senha é homologada diretamente pela Coordenação Geral do IV EFAC 2026.",
                size="1",
                color="#CBD5E1",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.box(
                rx.vstack(
                    rx.text(
                        "Para solicitar sua nova senha, envie uma mensagem à Coordenação:",
                        size="1",
                        color="#CBD5E1",
                    ),
                    rx.hstack(
                        rx.icon(tag="user", size=15, color="#00ADB5"),
                        rx.text("Prof. Dr. Edson Otoniel da Silva", size="1", weight="bold", color="white"),
                        spacing="1",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon(tag="mail", size=15, color="#38bdf8"),
                        rx.link(
                            "edson.otoniel@ufca.edu.br",
                            href="mailto:edson.otoniel@ufca.edu.br?subject=Solicita%C3%A7%C3%A3o%20de%20Redefini%C3%A7%C3%A3o%20de%20Senha%20-%20IV%20EFAC%202026&body=Prezado%20Prof.%20Dr.%20Edson%20Otoniel,%0D%0A%0D%0ASolicito%20a%20redefini%C3%A7%C3%A3o%20da%20minha%20senha%20de%20acesso%20ao%20portal%20do%20IV%20EFAC%202026.%0D%0A%0D%0AMeus%20dados%20cadastrais:%0D%0A-%20Nome%20Completo:%20%0D%0A-%20E-mail%20Cadastrado:%20%0D%0A%0D%0AAtenciosamente,",
                            size="1",
                            color="#38bdf8",
                            weight="bold",
                            underline="always",
                        ),
                        spacing="1",
                        align="center",
                    ),
                    rx.text(
                        "📌 Dica: Informe seu Nome Completo e E-mail cadastrado para agilizar o atendimento.",
                        size="1",
                        color="#CBD5E1",
                    ),
                    spacing="1",
                    align="start",
                ),
                padding="0.85rem",
                background="rgba(15, 23, 42, 0.75)",
                border="1px solid rgba(56, 189, 248, 0.25)",
                border_radius="8px",
                width="100%",
            ),
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon(tag="send", size=15),
                        rx.text("Enviar E-mail ao Prof. Otoniel"),
                        spacing="2",
                        align="center",
                    ),
                    size="2",
                    variant="soft",
                    color_scheme="cyan",
                    width="100%",
                    cursor="pointer",
                ),
                href="mailto:edson.otoniel@ufca.edu.br?subject=Solicita%C3%A7%C3%A3o%20de%20Redefini%C3%A7%C3%A3o%20de%20Senha%20-%20IV%20EFAC%202026&body=Prezado%20Prof.%20Dr.%20Edson%20Otoniel,%0D%0A%0D%0ASolicito%20a%20redefini%C3%A7%C3%A3o%20da%20minha%20senha%20de%20acesso%20ao%20portal%20do%20IV%20EFAC%202026.%0D%0A%0D%0AMeus%20dados%20cadastrais:%0D%0A-%20Nome%20Completo:%20%0D%0A-%20E-mail%20Cadastrado:%20%0D%0A%0D%0AAtenciosamente,",
                width="100%",
            ),
            spacing="2",
            width="100%",
        ),
        padding="1rem",
        background="rgba(11, 15, 25, 0.95)",
        border="1px solid rgba(56, 189, 248, 0.4)",
        border_radius="12px",
        box_shadow="0 8px 30px rgba(0, 0, 0, 0.5)",
        width="100%",
        margin_top="0.75rem",
    )


def form_login() -> rx.Component:
    return rx.vstack(
        feedback_alert(),
        rx.vstack(
            rx.text("E-mail Cadastrado", size="2", weight="bold", color="white"),
            rx.input(
                placeholder="seu.email@exemplo.com",
                type="email",
                value=AuthState.login_email,
                on_change=AuthState.set_login_email,
                size="3",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.vstack(
            rx.hstack(
                rx.text("Senha", size="2", weight="bold", color="white"),
                rx.spacer(),
                rx.link(
                    "Esqueceu sua senha?",
                    size="1",
                    color="#CBD5E1",
                    _hover={"color": "#38bdf8"},
                    cursor="pointer",
                    on_click=AuthState.toggle_aviso_recuperacao_senha,
                ),
                width="100%",
                align="center",
            ),
            rx.box(
                rx.input(
                    placeholder="Sua senha",
                    type=rx.cond(AuthState.mostrar_senha_login, "text", "password"),
                    value=AuthState.login_senha,
                    on_change=AuthState.set_login_senha,
                    size="3",
                    width="100%",
                    padding_right="2.5rem",
                ),
                rx.box(
                    rx.tooltip(
                        rx.icon(
                            tag=rx.cond(AuthState.mostrar_senha_login, "eye-off", "eye"),
                            size=18,
                            color="#CBD5E1",
                            _hover={"color": COLOR_CYAN},
                            cursor="pointer",
                            on_click=AuthState.toggle_mostrar_senha_login,
                        ),
                        content=rx.cond(AuthState.mostrar_senha_login, "Ocultar senha", "Ver senha"),
                    ),
                    position="absolute",
                    right="0.75rem",
                    top="50%",
                    transform="translateY(-50%)",
                    z_index="10",
                ),
                position="relative",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.button(
            "Acessar Minha Credencial",
            size="3",
            color_scheme="cyan",
            radius="full",
            width="100%",
            margin_top="1rem",
            on_click=AuthState.realizar_login,
            style=STYLE_BUTTON_CHIP,
        ),
        # Aviso institucional para redefinição de senha com Prof. Otoniel (exibido ao errar ou ao clicar no link)
        rx.cond(
            AuthState.mostrar_aviso_recuperacao_senha,
            card_recuperacao_senha(),
        ),
        spacing="3",
        width="100%",
    )
