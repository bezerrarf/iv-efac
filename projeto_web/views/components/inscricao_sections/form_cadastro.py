import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import *

from .feedback_alert import feedback_alert

def form_cadastro() -> rx.Component:
    return rx.vstack(
        feedback_alert(),
        rx.vstack(
            rx.text("Nome Completo", size="2", weight="bold", color="white"),
            rx.input(
                placeholder="Ex: Dra. Jocelyn Bell",
                value=EventoState.cad_nome,
                on_change=EventoState.set_cad_nome,
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
                value=EventoState.cad_email,
                on_change=EventoState.set_cad_email,
                size="3",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.vstack(
            rx.text("Senha de Acesso", size="2", weight="bold", color="white"),
            rx.input(
                placeholder="Crie uma senha (mínimo 6 caracteres)",
                type="password",
                value=EventoState.cad_senha,
                on_change=EventoState.set_cad_senha,
                size="3",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.grid(
            rx.vstack(
                rx.text("Instituição / Polo", size="2", weight="bold", color="white"),
                rx.input(
                    placeholder="Ex: UFCA, URCA, IFCE, etc.",
                    value=EventoState.cad_instituicao,
                    on_change=EventoState.set_cad_instituicao,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            rx.vstack(
                rx.text("Modalidade", size="2", weight="bold", color="white"),
                rx.select(
                    ["Presencial", "Online"],
                    value=EventoState.cad_modalidade,
                    on_change=EventoState.set_cad_modalidade,
                    size="3",
                    width="100%",
                ),
                spacing="1",
                width="100%",
            ),
            columns=rx.breakpoints(initial="1", sm="2"),
            spacing="3",
            width="100%",
        ),
        rx.vstack(
            rx.text("Eixo Temático de Interesse", size="2", weight="bold", color="white"),
            rx.select(
                [
                    "Astrofísica de Objetos Compactos",
                    "Relatividade Geral e Gravitação",
                    "Física Computacional e Ciência de Dados",
                    "Ensino de Física e Divulgação Científica",
                ],
                value=EventoState.cad_area,
                on_change=EventoState.set_cad_area,
                size="3",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.button(
            "Confirmar Inscrição Gratuita",
            size="3",
            color_scheme="indigo",
            radius="full",
            width="100%",
            margin_top="1rem",
            on_click=EventoState.realizar_cadastro,
            background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
            color="white",
            box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
            _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 22px rgba(0, 173, 181, 0.55)"},
            transition="all 0.2s ease",
            style=STYLE_BUTTON_CHIP,
        ),
        spacing="3",
        width="100%",
    )


