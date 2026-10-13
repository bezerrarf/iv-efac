"""Modal de Edição de Perfil, Segurança de Senha e Confirmação de E-mail."""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_SURFACE_GLASS,
    STYLE_BUTTON_CHIP,
    STYLE_TEXT_RESPONSIVE,
)


def modal_meu_perfil() -> rx.Component:
    """Modal central de gerenciamento de dados cadastrais, credenciais e e-mail."""
    return rx.cond(
        AuthState.modal_perfil_aberto,
        rx.box(
            # Fundo escuro com backdrop blur
            rx.box(
                position="fixed",
                top="0",
                left="0",
                width="100vw",
                height="100vh",
                background="rgba(2, 6, 23, 0.75)",
                backdrop_filter="blur(8px)",
                z_index="1000",
                on_click=AuthState.fechar_modal_perfil,
            ),
            # Conteúdo do Modal
            rx.box(
                rx.vstack(
                    # Cabeçalho do Modal
                    rx.hstack(
                        rx.hstack(
                            rx.icon(tag="user-cog", size=22, color=COLOR_CYAN),
                            rx.vstack(
                                rx.heading("Meu Perfil & Segurança", size="4", weight="bold", color="white"),
                                rx.text(
                                    f"{AuthState.user_nome} • {AuthState.user_codigo}",
                                    size="1",
                                    color="#CBD5E1",
                                ),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            size="1",
                            on_click=AuthState.fechar_modal_perfil,
                            cursor="pointer",
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.2"),
                    # Abas de Configuração
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="user", size=15),
                                    rx.text("Dados Pessoais", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="dados",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="key-round", size=15),
                                    rx.text("Troca de Senha", size="2"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="senha",
                            ),

                            
                            size="2",
                        ),
                        # Aba 1: Dados Pessoais
                        rx.tabs.content(
                            rx.vstack(
                                rx.vstack(
                                    rx.text("Nome Completo", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Seu nome completo",
                                        value=AuthState.perfil_nome_input,
                                        on_change=AuthState.set_perfil_nome,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Instituição de Ensino / Polo", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Ex: Universidade Federal do Cariri (UFCA)",
                                        value=AuthState.perfil_instituicao_input,
                                        on_change=AuthState.set_perfil_instituicao,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Modalidade de Participação", size="1", weight="bold", color="white"),
                                    rx.hstack(
                                        rx.button(
                                            "Presencial (Brejo Santo)",
                                            variant=rx.cond(AuthState.perfil_modalidade_input == "Presencial", "solid", "outline"),
                                            color_scheme="cyan",
                                            size="2",
                                            on_click=AuthState.set_perfil_modalidade("Presencial"),
                                        ),
                                        rx.button(
                                            "Online (Transmissão)",
                                            variant=rx.cond(AuthState.perfil_modalidade_input == "Online", "solid", "outline"),
                                            color_scheme="indigo",
                                            size="2",
                                            on_click=AuthState.set_perfil_modalidade("Online"),
                                        ),
                                        spacing="2",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="save", size=15),
                                            rx.text("Salvar Alterações"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="2",
                                        color_scheme="cyan",
                                        on_click=AuthState.salvar_meu_perfil,
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    width="100%",
                                    padding_top="0.8rem",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="dados",
                            padding_top="1rem",
                        ),
                        # Aba 2: Troca de Senha Segura
                        rx.tabs.content(
                            rx.vstack(
                                rx.text(
                                    "Para proteger sua conta, informe sua senha atual antes de cadastrar uma nova credencial.",
                                    size="2",
                                    color="#E2E8F0",
                                    style=STYLE_TEXT_RESPONSIVE,
                                ),
                                rx.vstack(
                                    rx.text("Senha Atual", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Digite sua senha atual",
                                        type="password",
                                        value=AuthState.minha_senha_atual_input,
                                        on_change=AuthState.set_minha_senha_atual,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Nova Senha (Mínimo 6 caracteres)", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Digite a nova senha",
                                        type="password",
                                        value=AuthState.minha_nova_senha_input,
                                        on_change=AuthState.set_minha_nova_senha,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.vstack(
                                    rx.text("Confirme a Nova Senha", size="1", weight="bold", color="white"),
                                    rx.input(
                                        placeholder="Repita a nova senha",
                                        type="password",
                                        value=AuthState.minha_nova_senha_confirm,
                                        on_change=AuthState.set_minha_nova_senha_confirm,
                                        size="2",
                                        width="100%",
                                    ),
                                    width="100%",
                                    align="start",
                                ),
                                rx.hstack(
                                    rx.spacer(),
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="lock", size=15),
                                            rx.text("Atualizar Senha"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="2",
                                        color_scheme="green",
                                        on_click=AuthState.salvar_minha_nova_senha,
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    width="100%",
                                    padding_top="0.8rem",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                            value="senha",
                            padding_top="1rem",
                        ),
                        default_value="dados",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="1001",
                width="92%",
                max_width="620px",
                max_height="90vh",
                overflow_y="auto",
                background="rgba(15, 23, 42, 0.98)",
                border="1.5px solid rgba(0, 173, 181, 0.4)",
                box_shadow="0 25px 60px rgba(0, 0, 0, 0.85)",
                border_radius="16px",
                padding="1.5rem",
            ),
        ),
        rx.fragment(),
    )
