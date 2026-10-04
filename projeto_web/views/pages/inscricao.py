"""Página de Inscrição, Login, Credencial e Submissões do IV EFAC (View).
Preserva persistência completa no SQLite em modo WAL e controle de sessão.
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import footer
from projeto_web.state.evento_state import EventoState


def templates_pos_inscricao() -> rx.Component:
    """Seção de templates liberada exclusivamente para participantes inscritos."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="file-down", size=20, color="#00ADB5"),
                rx.heading("Modelos Oficiais de Submissão", size="4", weight="bold"),
                align="center",
                spacing="2",
            ),
            rx.text(
                "Diretrizes e arquivos para envio de Resumo Expandido nos Anais do IV EFAC (11 e 12/11/2026).",
                size="2",
                color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
            ),
            rx.vstack(
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="file-text", size=18, color="#103460"),
                            rx.vstack(
                                rx.text("Modelo de Resumo Expandido (.docx)", size="2", weight="bold"),
                                rx.text("2 a 4 páginas com Introdução, Metodologia, Resultados e Referências", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar Modelo", color_scheme="cyan", size="1"),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
                    ),
                    href="#",
                    width="100%",
                ),
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="presentation", size=18, color="#00ADB5"),
                            rx.vstack(
                                rx.text("Slide para Apresentação Oral (15 min)", size="2", weight="bold"),
                                rx.text("Padrão 16:9 oficial com chancela UFCA e FUNCAP", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar PPTX", color_scheme="blue", size="1"),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
                    ),
                    href="#",
                    width="100%",
                ),
                rx.link(
                    rx.card(
                        rx.hstack(
                            rx.icon(tag="layout_grid", size=18, color="#2563EB"),
                            rx.vstack(
                                rx.text("Modelo de Pôster / Painel Científico", size="2", weight="bold"),
                                rx.text("Dimensão 90x120cm para exibição no hall do IFE", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            rx.spacer(),
                            rx.badge("Baixar Template", color_scheme="indigo", size="1"),
                            align="center",
                            width="100%",
                        ),
                        width="100%",
                        padding="0.75rem",
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
    """Card exibido quando o usuário está autenticado/inscrito."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="circle-check", size=24, color="#34d399"),
                rx.badge("Inscrição Confirmada • IV EFAC", color_scheme="green", variant="solid", size="2"),
                rx.spacer(),
                rx.badge(EventoState.user_modalidade, color_scheme="cyan", variant="soft", size="2"),
                align="center",
                width="100%",
            ),
            rx.divider(color_scheme="gray", opacity="0.2"),
            rx.hstack(
                rx.image(
                    src="/logo_ivefac.jpeg",
                    width="54px",
                    height="54px",
                    border_radius="50%",
                    object_fit="cover",
                    border="2px solid #00ADB5",
                    box_shadow="0 0 12px rgba(0, 173, 181, 0.4)",
                ),
                rx.vstack(
                    rx.text("Credencial Oficial de Participante", size="1", color="var(--gray-9)", text_transform="uppercase"),
                    rx.heading(
                        EventoState.user_nome,
                        size="6",
                        weight="bold",
                        color=rx.color_mode_cond(light="#103460", dark="white"),
                    ),
                    rx.text(EventoState.user_email, size="2", color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)")),
                    rx.hstack(
                        rx.icon(tag="building", size=16, color="#00ADB5"),
                        rx.text(EventoState.user_instituicao, size="2", color=rx.color_mode_cond(light="#334155", dark="var(--gray-11)")),
                        align="center",
                        spacing="1",
                    ),
                    align="start",
                    spacing="1",
                ),
                spacing="3",
                align="center",
                margin_y="0.5rem",
                width="100%",
            ),
            # Código da Inscrição em destaque
            rx.box(
                rx.vstack(
                    rx.text("Seu Código de Check-in no Campus Brejo Santo", size="1", color="#00ADB5"),
                    rx.heading(EventoState.user_codigo, size="7", weight="bold", color="#00ADB5", letter_spacing="2px"),
                    align="center",
                    spacing="0",
                ),
                background=rx.color_mode_cond(light="rgba(0, 173, 181, 0.08)", dark="rgba(0, 173, 181, 0.08)"),
                border="1px dashed rgba(0, 173, 181, 0.4)",
                border_radius="12px",
                padding="1rem",
                width="100%",
            ),
            # Ação de troca de modalidade
            rx.hstack(
                rx.text("Modalidade atual:", size="2", color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)")),
                rx.cond(
                    EventoState.user_modalidade == "Presencial",
                    rx.button(
                        "Mudar para Online",
                        size="1",
                        variant="outline",
                        color_scheme="cyan",
                        on_click=lambda: EventoState.alterar_modalidade_usuario("Online"),
                    ),
                    rx.button(
                        "Mudar para Presencial",
                        size="1",
                        variant="outline",
                        color_scheme="indigo",
                        on_click=lambda: EventoState.alterar_modalidade_usuario("Presencial"),
                    ),
                ),
                align="center",
                spacing="2",
            ),
            # Status do Certificado
            rx.box(
                rx.hstack(
                    rx.icon(tag="award", size=18, color="#f59e0b"),
                    rx.vstack(
                        rx.text("Certificado Oficial de Participação", size="2", weight="bold"),
                        rx.text("Disponível a partir de 12 de novembro de 2026 após as sessões de encerramento.", size="1", color="var(--gray-9)"),
                        spacing="0",
                        align="start",
                    ),
                    spacing="2",
                    align="center",
                ),
                background=rx.color_mode_cond(light="rgba(245, 158, 11, 0.08)", dark="rgba(245, 158, 11, 0.1)"),
                border="1px solid rgba(245, 158, 11, 0.2)",
                border_radius="10px",
                padding="0.75rem",
                width="100%",
            ),
            rx.divider(color_scheme="gray", opacity="0.2"),
            # Seção de Templates pós-inscrição
            templates_pos_inscricao(),
            rx.hstack(
                rx.button(
                    "Encerrar Sessão",
                    variant="outline",
                    color_scheme="red",
                    size="2",
                    on_click=EventoState.logout,
                ),
                justify="end",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        background=rx.color_mode_cond(light="#ffffff", dark="linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.85))"),
        backdrop_filter="blur(16px)",
        border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(0, 173, 181, 0.3)"),
        box_shadow="0 10px 40px rgba(0, 0, 0, 0.15)",
        padding="2rem",
        max_width="580px",
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


def form_cadastro() -> rx.Component:
    return rx.vstack(
        feedback_alert(),
        rx.vstack(
            rx.text("Nome Completo", size="2", weight="bold"),
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
            rx.text("E-mail Institucional ou Pessoal", size="2", weight="bold"),
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
            rx.text("Senha de Acesso", size="2", weight="bold"),
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
                rx.text("Instituição / Polo", size="2", weight="bold"),
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
                rx.text("Modalidade", size="2", weight="bold"),
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
            rx.text("Eixo Temático de Interesse", size="2", weight="bold"),
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
            background="#103460",
            color="white",
            box_shadow="0 4px 15px rgba(16, 52, 96, 0.4)",
            _hover={"transform": "translateY(-1px)", "background": "#16457e"},
            transition="all 0.2s ease",
        ),
        spacing="3",
        width="100%",
    )


def form_login() -> rx.Component:
    return rx.vstack(
        feedback_alert(),
        rx.vstack(
            rx.text("E-mail Cadastrado", size="2", weight="bold"),
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
            rx.text("Senha", size="2", weight="bold"),
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
        ),
        spacing="3",
        width="100%",
    )


def inscricao_page() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.vstack(
                rx.image(
                    src="/logo_ivefac.jpeg",
                    width="72px",
                    height="72px",
                    border_radius="50%",
                    object_fit="cover",
                    border="2px solid #00ADB5",
                    box_shadow="0 0 20px rgba(0, 173, 181, 0.35)",
                    margin_bottom="0.2rem",
                ),
                rx.badge("Portal de Credenciamento Oficial • IV EFAC", color_scheme="cyan", variant="soft", size="2"),
                rx.heading(
                    "Inscrição & Credencial do Evento",
                    size="8",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="white"),
                ),
                rx.text(
                    "Cadastre-se gratuitamente para garantir sua vaga presencial no Campus Brejo Santo ou receber os links da transmissão online.",
                    size="3",
                    color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    text_align="center",
                    max_width="650px",
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
                        background=rx.color_mode_cond(light="#ffffff", dark="rgba(15, 23, 42, 0.85)"),
                        backdrop_filter="blur(16px)",
                        border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.08)"),
                        padding="2rem",
                        max_width="540px",
                        width="100%",
                        box_shadow="0 10px 40px rgba(0, 0, 0, 0.12)",
                    ),
                ),
                align="center",
                spacing="4",
                max_width="1100px",
                margin="0 auto",
                padding="3rem 1.5rem 5rem 1.5rem",
            ),
            width="100%",
        ),
        footer(),
        min_height="100vh",
        background=rx.color_mode_cond(light="#f8fafc", dark="#060814"),
        color=rx.color_mode_cond(light="#0f172a", dark="white"),
        transition="background 0.3s ease, color 0.3s ease",
    )
