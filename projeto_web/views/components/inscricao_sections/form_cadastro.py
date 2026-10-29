import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

from .feedback_alert import feedback_alert


def form_cadastro() -> rx.Component:
    return rx.form(
        rx.vstack(
            feedback_alert(),
            rx.vstack(
                rx.text("Nome Completo", size="2", weight="bold", color="white"),
                rx.input(
                    placeholder="Ex.: Dra. Jocelyn Bell Burnell",
                    name="nome",
                    value=AuthState.cad_nome,
                    on_change=AuthState.set_cad_nome,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("E-mail Institucional ou Pessoal", size="2", weight="bold", color="white"),
                rx.input(
                    placeholder="seu.email@exemplo.com",
                    type="email",
                    name="email",
                    value=AuthState.cad_email,
                    on_change=AuthState.set_cad_email,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("Senha de Acesso", size="2", weight="bold", color="white"),
                rx.box(
                    rx.input(
                        placeholder="Crie uma senha (mínimo de 6 caracteres)",
                        type=rx.cond(AuthState.mostrar_senha_cad, "text", "password"),
                        name="senha",
                        value=AuthState.cad_senha,
                        on_change=AuthState.set_cad_senha,
                        size="3",
                        width="100%",
                        padding_right="2.5rem",
                    ),
                    rx.box(
                        rx.tooltip(
                            rx.icon(
                                tag=rx.cond(AuthState.mostrar_senha_cad, "eye-off", "eye"),
                                size=18,
                                color="#CBD5E1",
                                _hover={"color": COLOR_CYAN},
                                cursor="pointer",
                                on_click=AuthState.toggle_mostrar_senha_cad,
                            ),
                            content=rx.cond(AuthState.mostrar_senha_cad, "Ocultar senha", "Ver senha"),
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
            rx.vstack(
                rx.text("Instituição / Polo Acadêmico", size="2", weight="bold", color="white"),
                rx.input(
                    placeholder="Ex.: UFCA, URCA, IFCE, UFC, etc.",
                    name="instituicao",
                    value=AuthState.cad_instituicao,
                    on_change=AuthState.set_cad_instituicao,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("Eixo Temático de Interesse", size="2", weight="bold", color="white"),
                rx.select(
                    [
                        "Astrofísica",
                        "Física Computacional",
                        "Relatividade e Gravitação",
                        "Física Quântica",
                        "Ensino e Divulgação Científica",
                    ],
                    value=AuthState.cad_area,
                    on_change=AuthState.set_cad_area,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.button(
                "Confirmar Inscrição Gratuita",
                type="submit",
                size="3",
                color_scheme="indigo",
                radius="full",
                width="100%",
                margin_top="1rem",
                background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                color="white",
                box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 22px rgba(0, 173, 181, 0.55)"},
                transition="all 0.2s ease",
                style=STYLE_BUTTON_CHIP,
            ),
            spacing="3",
            width="100%",
        ),
        on_submit=AuthState.realizar_cadastro_form,
        width="100%",
    )
