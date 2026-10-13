import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

from .feedback_alert import feedback_alert

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
            rx.text("Senha", size="2", weight="bold", color="white"),
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
                            color="var(--gray-9)",
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
        spacing="3",
        width="100%",
    )


