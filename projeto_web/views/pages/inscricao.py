"""Página de Inscrição, Login, Credencial e Submissões do IV EFAC (View - UI/UX Pro Max).
Preserva persistência completa no SQLite em modo WAL e controle de sessão.
Pure Deep Cosmic Dark Theme com responsividade completa para todas as telas.
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import (
    COLOR_BG,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_SUBTLE,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
    STYLE_BUTTON_CHIP,
)


def templates_pos_inscricao() -> rx.Component:
    """Seção de templates liberada exclusivamente para participantes inscritos."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="file-down", size=20, color=COLOR_CYAN),
                rx.heading("Modelos Oficiais de Submissão", size="4", weight="bold", color="white", style=STYLE_HEADING_RESPONSIVE),
                align="center",
                spacing="2",
            ),
            rx.text(
                "Diretrizes e arquivos para envio de Resumo Expandido nos Anais do IV EFAC (11 e 12/11/2026).",
                size="2",
                color="var(--gray-10)",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.vstack(
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="file-text", size=18, color=COLOR_CYAN),
                            rx.vstack(
                                rx.text("Modelo de Resumo Expandido (.docx)", size="2", weight="bold", color="white"),
                                rx.text("2 a 4 páginas com Introdução, Metodologia, Resultados e Referências", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar Modelo", color_scheme="cyan", size="1", style=STYLE_BUTTON_CHIP),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
                        background="rgba(15, 23, 42, 0.6)",
                        border="1px solid rgba(255, 255, 255, 0.08)",
                        _hover={"border_color": COLOR_CYAN, "transform": "translateY(-1px)"},
                        transition="all 0.2s ease",
                    ),
                    href="#",
                    width="100%",
                ),
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="presentation", size=18, color=COLOR_CYAN_LIGHT),
                            rx.vstack(
                                rx.text("Slide para Apresentação Oral (15 min)", size="2", weight="bold", color="white"),
                                rx.text("Padrão 16:9 oficial com chancela UFCA e FUNCAP", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar PPTX", color_scheme="blue", size="1", style=STYLE_BUTTON_CHIP),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
                        background="rgba(15, 23, 42, 0.6)",
                        border="1px solid rgba(255, 255, 255, 0.08)",
                        _hover={"border_color": COLOR_CYAN_LIGHT, "transform": "translateY(-1px)"},
                        transition="all 0.2s ease",
                    ),
                    href="#",
                    width="100%",
                ),
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="layout-grid", size=18, color="#818CF8"),
                            rx.vstack(
                                rx.text("Modelo de Pôster / Painel Científico", size="2", weight="bold", color="white"),
                                rx.text("Dimensão 90x120cm para exibição no hall do IFE", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar Template", color_scheme="indigo", size="1", style=STYLE_BUTTON_CHIP),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
                        background="rgba(15, 23, 42, 0.6)",
                        border="1px solid rgba(255, 255, 255, 0.08)",
                        _hover={"border_color": "#818CF8", "transform": "translateY(-1px)"},
                        transition="all 0.2s ease",
                    ),
                    href="#",
                    width="100%",
                ),
                width="100%",
                spacing="2",
            ),
            spacing="3",
            width="100%",
            padding_top="1rem",
        ),
        width="100%",
    )


def credencial_card() -> rx.Component:
    """Card exibido quando o usuário está autenticado/inscrito (Deep Cosmic Glass)."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="circle-check", size=24, color="#34d399"),
                rx.badge("Inscrição Confirmada • IV EFAC", color_scheme="green", variant="solid", size="2", style=STYLE_BUTTON_CHIP),
                rx.spacer(),
                rx.badge(EventoState.user_modalidade, color_scheme="cyan", variant="soft", size="2", style=STYLE_BUTTON_CHIP),
                align="center",
                width="100%",
                wrap="wrap",
                gap="2",
            ),
            rx.divider(color_scheme="gray", opacity="0.18"),
            rx.vstack(
                rx.text("Credencial Oficial de Participante", size="1", color="var(--gray-9)", text_transform="uppercase", letter_spacing="0.1em"),
                rx.heading(
                    EventoState.user_nome,
                    size=rx.breakpoints(initial="5", sm="6"),
                    weight="bold",
                    color="white",
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(EventoState.user_email, size="2", color="var(--gray-10)", style=STYLE_TEXT_RESPONSIVE),
                rx.hstack(
                    rx.icon(tag="building", size=16, color=COLOR_CYAN),
                    rx.text(EventoState.user_instituicao, size="2", color="var(--gray-11)", style=STYLE_TEXT_RESPONSIVE),
                    align="center",
                    spacing="1",
                ),
                align="start",
                spacing="1",
                margin_y="0.5rem",
                width="100%",
            ),
            # Código da Inscrição em destaque
            rx.box(
                rx.vstack(
                    rx.text("Seu Código de Check-in no Campus Brejo Santo", size="1", color=COLOR_CYAN, style=STYLE_TEXT_RESPONSIVE),
                    rx.heading(EventoState.user_codigo, size=rx.breakpoints(initial="6", sm="7"), weight="bold", color=COLOR_CYAN, letter_spacing="2px"),
                    align="center",
                    spacing="0",
                ),
                background="rgba(0, 173, 181, 0.08)",
                border="1px dashed rgba(0, 173, 181, 0.45)",
                border_radius="12px",
                padding="1rem",
                width="100%",
            ),
            # Ação de troca de modalidade com ID explícito para automação e feedback imediato
            rx.hstack(
                rx.text("Modalidade atual:", size="2", color="var(--gray-10)"),
                rx.cond(
                    EventoState.user_modalidade == "Presencial",
                    rx.button(
                        "Mudar para Online",
                        id="btn-alternar-modalidade",
                        size="1",
                        variant="outline",
                        color_scheme="cyan",
                        on_click=lambda: EventoState.alterar_modalidade_usuario("Online"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.button(
                        "Mudar para Presencial",
                        id="btn-alternar-modalidade",
                        size="1",
                        variant="outline",
                        color_scheme="indigo",
                        on_click=lambda: EventoState.alterar_modalidade_usuario("Presencial"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                ),
                align="center",
                spacing="2",
                wrap="wrap",
            ),
            # Status do Certificado
            rx.box(
                rx.hstack(
                    rx.icon(tag="award", size=18, color="#f59e0b"),
                    rx.vstack(
                        rx.text("Certificado Oficial de Participação", size="2", weight="bold", color="white"),
                        rx.text("Disponível a partir de 12 de novembro de 2026 após as sessões de encerramento.", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                        spacing="0",
                        align="start",
                    ),
                    spacing="2",
                    align="center",
                ),
                background="rgba(245, 158, 11, 0.08)",
                border="1px solid rgba(245, 158, 11, 0.2)",
                border_radius="10px",
                padding="0.75rem",
                width="100%",
            ),
            rx.divider(color_scheme="gray", opacity="0.18"),
            # Seção de Templates pós-inscrição
            templates_pos_inscricao(),
            rx.hstack(
                rx.button(
                    "Encerrar Sessão",
                    variant="outline",
                    color_scheme="red",
                    size="2",
                    on_click=EventoState.logout,
                    style=STYLE_BUTTON_CHIP,
                ),
                justify="end",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        background="linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85))",
        backdrop_filter="blur(16px)",
        border="1px solid rgba(0, 173, 181, 0.3)",
        box_shadow="0 12px 45px rgba(0, 0, 0, 0.45)",
        padding=rx.breakpoints(initial="1.25rem", sm="2rem"),
        max_width="580px",
        width="100%",
        border_radius="16px",
    )


def feedback_alert() -> rx.Component:
    return rx.cond(
        EventoState.feedback_msg != "",
        rx.callout(
            EventoState.feedback_msg,
            icon=rx.cond(EventoState.feedback_tipo == "success", "circle-check", "alert-circle"),
            color_scheme=rx.cond(EventoState.feedback_tipo == "success", "green", "red"),
            variant="soft",
            size="2",
            width="100%",
            margin_bottom="1rem",
        ),
    )


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
            radius="full",
            width="100%",
            margin_top="1rem",
            on_click=EventoState.realizar_cadastro,
            background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
            color="white",
            box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
            _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.55)"},
            transition="all 0.2s ease",
            style=STYLE_BUTTON_CHIP,
        ),
        spacing="3",
        width="100%",
    )


def form_login() -> rx.Component:
    return rx.vstack(
        feedback_alert(),
        rx.vstack(
            rx.text("E-mail Cadastrado", size="2", weight="bold", color="white"),
            rx.input(
                placeholder="seu.email@exemplo.com",
                type="email",
                value=EventoState.login_email,
                on_change=EventoState.set_login_email,
                size="3",
                width="100%",
            ),
            spacing="1",
            width="100%",
        ),
        rx.vstack(
            rx.text("Senha", size="2", weight="bold", color="white"),
            rx.input(
                placeholder="Sua senha",
                type="password",
                value=EventoState.login_senha,
                on_change=EventoState.set_login_senha,
                size="3",
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
            on_click=EventoState.realizar_login,
            style=STYLE_BUTTON_CHIP,
        ),
        spacing="3",
        width="100%",
    )


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
                    EventoState.is_logged_in,
                    credencial_card(),
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
