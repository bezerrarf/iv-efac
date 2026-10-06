"""Página de Inscrição, Login, Credencial e Submissões do IV EFAC (View - UI/UX Pro Max).
Preserva persistência completa no SQLite em modo WAL e controle de sessão.
Pure Deep Cosmic Dark Theme com responsividade e flexibilidade completa.
Inclui:
- Cartão de Identificação Digital Oficial baseado em WhatsApp Image 2026-10-03 at 16.05.42
- Painel Administrativo com análise de participantes, concessão de supervisores e editor de grade
- Painel de Supervisão para conferência de presença durante as atividades do evento
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.views.components.badge_card import cartao_identificacao_digital
from projeto_web.views.components.painel_admin import painel_admin_view
from projeto_web.views.components.painel_supervisor import painel_supervisor_view
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
    """Seção de templates e submissão liberada após a confirmação do e-mail."""
    conteudo_liberado = rx.vstack(
        rx.hstack(
            rx.icon(tag="file-down", size=20, color=COLOR_CYAN),
            rx.heading("Modelos Oficiais de Submissão", size="4", weight="bold", color="white"),
            rx.spacer(),
            rx.badge("E-mail Verificado • Submissão Liberada", color_scheme="green", variant="solid", size="1"),
            align="center",
            width="100%",
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
                        rx.icon(tag="presentation", size=18, color="#818CF8"),
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
                    _hover={"border_color": "#818CF8", "transform": "translateY(-1px)"},
                    transition="all 0.2s ease",
                ),
                href="#",
                width="100%",
            ),
            rx.link(
                rx.card(
                    rx.hstack(
                        rx.icon(tag="layout-grid", size=18, color="#34d399"),
                        rx.vstack(
                            rx.text("Modelo de Pôster / Painel Científico", size="2", weight="bold", color="white"),
                            rx.text("Dimensão 90x120cm para exibição no hall do IFE", size="1", color="var(--gray-9)", style=STYLE_TEXT_RESPONSIVE),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Baixar Template", color_scheme="green", size="1", style=STYLE_BUTTON_CHIP),
                        align="center",
                        width="100%",
                    ),
                    width="100%",
                    padding="0.75rem",
                    background="rgba(15, 23, 42, 0.6)",
                    border="1px solid rgba(255, 255, 255, 0.08)",
                    _hover={"border_color": "#34d399", "transform": "translateY(-1px)"},
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
    )

    aviso_bloqueio_email = rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="mail-warning", size=24, color="#F59E0B"),
                rx.heading("Confirmação de E-mail Necessária para Submissões", size="3", weight="bold", color="white"),
                rx.spacer(),
                rx.badge("Ação Requerida", color_scheme="amber", variant="solid", size="1"),
                align="center",
                width="100%",
                spacing="2",
            ),
            rx.text(
                "Olá, pesquisador(a)! Para garantir a integridade acadêmica do evento e liberar o envio de artigos e o download dos templates oficiais, é necessário confirmar seu endereço de e-mail.",
                size="2",
                color="var(--gray-11)",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.callout(
                "⚠️ Aviso Importante sobre Caixa de Spam / Lixo Eletrônico: Mensagens automáticas com códigos de verificação podem ser filtradas como spam pelo seu provedor (Gmail, Hotmail, etc.). Por favor, verifique sua pasta de Spam ou Lixo Eletrônico e marque o remetente oficial como 'Não é Spam' / 'Remetente Confiável' para nunca perder os pareceres das bancas e comunicados do simpósio.",
                icon="shield-alert",
                color_scheme="amber",
                variant="soft",
                size="2",
                width="100%",
            ),
            rx.hstack(
                rx.button(
                    rx.icon(tag="mail-check", size=16),
                    "Confirmar Meu E-mail Agora",
                    on_click=EventoState.abrir_modal_perfil,
                    color_scheme="amber",
                    size="2",
                    cursor="pointer",
                ),
                rx.button(
                    rx.icon(tag="check", size=16),
                    "Verificação Direta Instantânea",
                    on_click=EventoState.confirmar_email_direto,
                    variant="soft",
                    color_scheme="green",
                    size="2",
                    cursor="pointer",
                ),
                spacing="3",
                wrap="wrap",
            ),
            spacing="3",
            width="100%",
        ),
        width="100%",
        padding="1.25rem",
        background="rgba(245, 158, 11, 0.08)",
        border="1px solid rgba(245, 158, 11, 0.3)",
        border_radius="12px",
    )

    return rx.box(
        rx.cond(
            EventoState.email_confirmado,
            conteudo_liberado,
            aviso_bloqueio_email,
        ),
        width="100%",
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


def logged_in_hub() -> rx.Component:
    """Hub interativo do participante, supervisor e administrador autenticado."""
    return rx.vstack(
        feedback_alert(),
        # Barra Superior de Status do Usuário
        rx.hstack(
            rx.hstack(
                rx.cond(
                    EventoState.user_foto_url != "",
                    rx.image(
                        src=EventoState.user_foto_url,
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
                        rx.heading(EventoState.user_nome, size="3", weight="bold", color="white"),
                        rx.cond(
                            EventoState.is_admin,
                            rx.badge("ADMIN", color_scheme="red", variant="solid", size="1"),
                            rx.cond(
                                EventoState.is_supervisor,
                                rx.badge("SUPERVISOR(A)", color_scheme="violet", variant="solid", size="1"),
                                rx.badge("PARTICIPANTE", color_scheme="cyan", variant="solid", size="1"),
                            ),
                        ),
                        spacing="2",
                        align="center",
                        wrap="wrap",
                    ),
                    rx.text(
                        EventoState.user_email,
                        " • ",
                        EventoState.user_instituicao,
                        " (",
                        EventoState.user_modalidade,
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
                    EventoState.user_modalidade == "Presencial",
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
                    on_click=EventoState.logout,
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
                    EventoState.is_admin,
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
                    EventoState.is_supervisor,
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
                    logged_in_hub(),
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
