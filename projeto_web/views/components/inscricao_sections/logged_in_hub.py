"""Hub interativo oficial do participante, supervisor e administrador autenticado - IV EFAC 2026.
Área do usuário reestruturada com:
1. Remoção da aba de crachá/carteirinha.
2. Nova aba com Lista de Inscrições / Atividades Disponíveis do Evento.
3. Submissão de Trabalhos & Modelos integrados diretamente no painel.
4. Alteração de Nome de Usuário e Modalidade em tempo real.
5. Solicitação transparente de confirmação de e-mail para emissão dos Certificados Oficiais (30h).
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.state.admin_state import AdminState
from projeto_web.state.supervisor_state import SupervisorState
from projeto_web.controllers.evento_controller import EventoController, Atividade
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    STYLE_BUTTON_CHIP,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)

from projeto_web.views.components.painel_admin import painel_admin_view
from projeto_web.views.components.painel_supervisor import painel_supervisor_view
from .templates_pos_inscricao import templates_pos_inscricao
from .feedback_alert import feedback_alert


def _card_atividade_disponivel(item: Atividade) -> rx.Component:
    """Card individual de palestra ou minicurso disponível para inscrição do congressista."""
    return rx.card(
        rx.hstack(
            rx.badge(item.horario, color_scheme="cyan", variant="solid", size="1", style=STYLE_BUTTON_CHIP),
            rx.vstack(
                rx.hstack(
                    rx.badge(item.dia, color_scheme="indigo", variant="surface", size="1", style=STYLE_BUTTON_CHIP),
                    rx.badge(item.tipo, color_scheme=item.tipo_color, size="1", variant="soft", style=STYLE_BUTTON_CHIP),
                    rx.text(item.local, size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                    spacing="2",
                    align="center",
                    wrap="wrap",
                ),
                rx.text(item.titulo, size="2", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                rx.text(item.palestrante, size="1", color=COLOR_CYAN_LIGHT, style=STYLE_TEXT_RESPONSIVE),
                spacing="0",
                align="start",
                width="100%",
            ),
            rx.spacer(),
            rx.badge(
                rx.hstack(
                    rx.icon(tag="check-check", size=13),
                    rx.text("Inscrição Inclusa"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="green",
                variant="soft",
                size="1",
                style=STYLE_BUTTON_CHIP,
            ),
            align="center",
            spacing="3",
            width="100%",
            wrap="wrap",
            gap="2",
        ),
        padding="0.9rem",
        width="100%",
        border_radius="12px",
        background="rgba(15, 23, 42, 0.7)",
        backdrop_filter="blur(16px)",
        border=f"1px solid {COLOR_BORDER_CYAN}",
        box_shadow="0 4px 18px rgba(0, 0, 0, 0.3)",
    )


def lista_inscricoes_disponiveis() -> rx.Component:
    """Aba com o catálogo de atividades e minicursos disponíveis do simpósio."""
    dia1 = EventoController.obter_programacao("Dia 1")
    dia2 = EventoController.obter_programacao("Dia 2")

    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.icon(tag="calendar-check", size=22, color=COLOR_CYAN),
                background="rgba(0, 173, 181, 0.15)",
                border_radius="8px",
                padding="0.5rem",
                display="grid",
                place_items="center",
            ),
            rx.vstack(
                rx.heading("Inscrições & Atividades Disponíveis do IV EFAC", size="4", weight="bold", color="white"),
                rx.text("Sua credencial concede acesso pleno a todas as conferências, mesas-redondas e sessões científicas.", size="2", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        # Seletor de Dias e Download Oficial do PDF da Programação
        rx.hstack(
            rx.hstack(
                rx.button(
                    "Dia 1 • 11/Nov (Abertura, Plenárias e Apresentações)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 1", "solid", "outline"),
                    color_scheme="cyan",
                    on_click=EventoState.set_dia("Dia 1"),
                    radius="full",
                    size="2",
                    style=STYLE_BUTTON_CHIP,
                ),
                rx.button(
                    "Dia 2 • 12/Nov (Mesas Temáticas e Encerramento)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 2", "solid", "outline"),
                    color_scheme="cyan",
                    on_click=EventoState.set_dia("Dia 2"),
                    radius="full",
                    size="2",
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="2",
                wrap="wrap",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon(tag="file-down", size=15),
                    rx.text("Baixar PDF da Programação", size="2", weight="bold"),
                    spacing="1",
                    align="center",
                ),
                variant="solid",
                color_scheme="cyan",
                on_click=EventoState.baixar_pdf_programacao,
                radius="full",
                size="2",
                style=STYLE_BUTTON_CHIP,
                box_shadow="0 4px 14px rgba(0, 173, 181, 0.35)",
            ),
            width="100%",
            align="center",
            wrap="wrap",
            gap="2",
        ),
        # Lista de Atividades
        rx.box(
            rx.cond(
                EventoState.dia_selecionado == "Dia 1",
                rx.vstack(*[_card_atividade_disponivel(item) for item in dia1], spacing="2", width="100%"),
                rx.vstack(*[_card_atividade_disponivel(item) for item in dia2], spacing="2", width="100%"),
            ),
            width="100%",
            max_height="520px",
            overflow_y="auto",
            padding_right="0.5rem",
        ),
        spacing="3",
        width="100%",
    )


def alerta_certificado_email() -> rx.Component:
    """Card informativo oficial para emissão de certificados oficiais."""
    return rx.card(
        rx.hstack(
            rx.icon(tag="award", size=22, color="#34d399"),
            rx.vstack(
                rx.heading("Certificado Oficial Homologado", size="3", weight="bold", color="#34d399"),
                rx.text(
                    "Cadastro ativo e homologado! A emissão digital com código de autenticidade será liberada automaticamente após a confirmação de presença no evento.",
                    size="1",
                    color="#CBD5E1",
                    style=STYLE_TEXT_RESPONSIVE,
                ),
                spacing="0",
                align="start",
            ),
            align="center",
            spacing="3",
            width="100%",
        ),
        padding="1rem 1.25rem",
        background="rgba(52, 211, 153, 0.08)",
        border="1px solid rgba(52, 211, 153, 0.3)",
        border_radius="12px",
        width="100%",
    )


def logged_in_hub() -> rx.Component:
    """Hub completo da Área do Usuário (Congressistas, Supervisores e Administradores)."""
    return rx.vstack(
        feedback_alert(),

        # Barra Superior de Identificação e Edição de Perfil
        rx.hstack(
            rx.hstack(
                rx.cond(
                    AuthState.user_foto_url != "",
                    rx.image(
                        src=AuthState.user_foto_url,
                        width="46px",
                        height="46px",
                        border_radius="50%",
                        object_fit="cover",
                        border="1.5px solid #00ADB5",
                    ),
                    rx.box(
                        rx.icon(tag="user", size=22, color=COLOR_CYAN),
                        background="rgba(0, 173, 181, 0.15)",
                        border_radius="50%",
                        padding="0.6rem",
                        display="grid",
                        place_items="center",
                    ),
                ),
                rx.vstack(
                    rx.hstack(
                        rx.heading(AuthState.user_nome, size="4", weight="bold", color="white"),
                        rx.cond(
                            AuthState.is_admin,
                            rx.badge("ADMINISTRADOR", color_scheme="red", variant="solid", size="1"),
                            rx.cond(
                                AuthState.is_supervisor,
                                rx.badge("SUPERVISOR(A)", color_scheme="violet", variant="solid", size="1"),
                                rx.badge("CONGRESSISTA", color_scheme="cyan", variant="solid", size="1"),
                            ),
                        ),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.hstack(
                        rx.text(AuthState.user_email, size="1", color="#CBD5E1"),
                        rx.text("•", size="1", color="var(--gray-8)"),
                        rx.text(AuthState.user_instituicao, size="1", color="#CBD5E1"),
                        rx.text("•", size="1", color="var(--gray-8)"),
                        rx.badge(AuthState.user_modalidade, color_scheme="indigo", variant="surface", size="1"),
                        rx.badge(AuthState.user_codigo, color_scheme="gray", variant="soft", size="1"),
                        spacing="1",
                        align="center",
                        wrap="wrap",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.spacer(),
            # Ações Rápidas: Editar Perfil / Modalidade e Sair
            rx.hstack(
                rx.tooltip(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="user-cog", size=14),
                            rx.text("Editar Dados", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        variant="surface",
                        color_scheme="cyan",
                        on_click=AuthState.abrir_modal_perfil,
                        style=STYLE_BUTTON_CHIP,
                    ),
                    content="Alterar Nome Completo, Modalidade ou Senha",
                ),
                rx.cond(
                    AuthState.user_modalidade == "Presencial",
                    rx.button(
                        "Mudar p/ Online",
                        size="2",
                        variant="outline",
                        color_scheme="cyan",
                        on_click=EventoState.alterar_modalidade_usuario("Online"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.button(
                        "Mudar p/ Presencial",
                        size="2",
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
                wrap="wrap",
            ),
            width="100%",
            align="center",
            padding="1.1rem 1.35rem",
            background="rgba(15, 23, 42, 0.85)",
            border="1px solid rgba(0, 173, 181, 0.25)",
            border_radius="14px",
            box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
            wrap="wrap",
            gap="2",
        ),

        # Alerta Pedagógico para Certificados (exibido apenas para participantes; oculto para o Administrador)
        rx.cond(~AuthState.is_admin, alerta_certificado_email()),

        # Abas da Área do Usuário
        rx.tabs.root(
            rx.tabs.list(
                rx.tabs.trigger(
                    rx.hstack(
                        rx.icon(tag="calendar-check", size=15),
                        rx.text("Atividades & Inscrições", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    value="atividades",
                ),
                rx.tabs.trigger(
                    rx.hstack(
                        rx.icon(tag="file-text", size=15),
                        rx.text("Submissões & Modelos", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    value="submissoes",
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
                        on_click=AdminState.carregar_painel_admin,
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
                        on_click=SupervisorState.carregar_painel_supervisor,
                    ),
                    rx.fragment(),
                ),
                size="2",
            ),
            rx.tabs.content(
                lista_inscricoes_disponiveis(),
                value="atividades",
                padding_top="1.5rem",
                width="100%",
            ),
            rx.tabs.content(
                templates_pos_inscricao(),
                value="submissoes",
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
            default_value="atividades",
            width="100%",
        ),
        spacing="4",
        width="100%",
        max_width="1020px",
    )
