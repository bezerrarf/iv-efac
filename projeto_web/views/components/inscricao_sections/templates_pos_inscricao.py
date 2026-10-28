import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

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
            color="#CBD5E1",
            style=STYLE_TEXT_RESPONSIVE,
        ),
        # Card Destacado para Submissão Oficial via Google Forms
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag="file-up", size=22, color=COLOR_CYAN),
                        background="rgba(0, 173, 181, 0.15)",
                        border_radius="8px",
                        padding="0.5rem",
                        display="grid",
                        place_items="center",
                    ),
                    rx.vstack(
                        rx.heading("Submissão Oficial de Artigos & Resumos", size="3", weight="bold", color="white"),
                        rx.text("Envie seu trabalho diretamente para o Comitê Científico através do formulário institucional.", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="external-link", size=16),
                            rx.text("Acessar Formulário Oficial de Submissão (Google Forms)", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        size="3",
                        radius="full",
                        background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                        color="white",
                        box_shadow="0 4px 18px rgba(0, 173, 181, 0.45)",
                        _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.6)"},
                        transition="all 0.2s ease",
                        width="100%",
                        style=STYLE_BUTTON_CHIP,
                    ),
                    href="https://forms.gle/MrVPgHYqPGWaKd26A",
                    is_external=True,
                    width="100%",
                ),
                spacing="3",
                width="100%",
            ),
            padding="1.25rem",
            background="linear-gradient(145deg, rgba(0, 173, 181, 0.12), rgba(16, 52, 96, 0.25))",
            border=f"1.5px solid {COLOR_BORDER_CYAN}",
            border_radius="14px",
            width="100%",
        ),
        rx.vstack(
            rx.link(
                rx.card(
                    rx.hstack(
                        rx.icon(tag="file-text", size=18, color=COLOR_CYAN),
                        rx.vstack(
                            rx.text("Modelo de Resumo Expandido (.docx)", size="2", weight="bold", color="white"),
                            rx.text("2 a 4 páginas com Introdução, Metodologia, Resultados e Referências", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
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
                href=EventoState.link_modelo_resumo,
                is_external=True,
                width="100%",
            ),
            rx.link(
                rx.card(
                    rx.hstack(
                        rx.icon(tag="presentation", size=18, color="#818CF8"),
                        rx.vstack(
                            rx.text("Slide para Apresentação Oral (15 min)", size="2", weight="bold", color="white"),
                            rx.text("Padrão 16:9 oficial com chancela UFCA e FUNCAP", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
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
                href=EventoState.link_modelo_slides,
                is_external=True,
                width="100%",
            ),
            rx.link(
                rx.card(
                    rx.hstack(
                        rx.icon(tag="layout-grid", size=18, color="#34d399"),
                        rx.vstack(
                            rx.text("Modelo de Pôster / Painel Científico", size="2", weight="bold", color="white"),
                            rx.text("Dimensão 90x120cm para exibição no hall do IFE", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
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
                href=EventoState.link_modelo_poster,
                is_external=True,
                width="100%",
            ),
            rx.link(
                rx.card(
                    rx.hstack(
                        rx.icon(tag="book-open-check", size=20, color="#F59E0B"),
                        rx.vstack(
                            rx.hstack(
                                rx.text("Normas Oficiais de Submissão de Trabalhos (PDF)", size="2", weight="bold", color="white"),
                                rx.badge("Documento Oficial", color_scheme="amber", size="1"),
                                spacing="2",
                                align="center",
                            ),
                            rx.text("Consulte as diretrizes completas de formatação, limites de páginas (resumo expandido), pôsteres e cronograma", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Acessar Normas", color_scheme="amber", size="1", style=STYLE_BUTTON_CHIP),
                        align="center",
                        width="100%",
                    ),
                    width="100%",
                    padding="0.75rem",
                    background="rgba(245, 158, 11, 0.08)",
                    border="1px solid rgba(245, 158, 11, 0.3)",
                    _hover={"border_color": "#F59E0B", "transform": "translateY(-1px)", "background": "rgba(245, 158, 11, 0.14)"},
                    transition="all 0.2s ease",
                ),
                href="/normas-submissao",
                width="100%",
            ),
            width="100%",
            spacing="2",
        ),
        # Painel Administrativo para Edição dos Links dos Modelos
        rx.cond(
            AuthState.is_admin,
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="settings", size=18, color=COLOR_CYAN),
                        rx.heading("Gerenciar Links dos Modelos (Acesso do Administrador)", size="3", weight="bold", color="white"),
                        rx.spacer(),
                        rx.badge("Painel Admin", color_scheme="red", size="1"),
                        align="center",
                        width="100%",
                        spacing="2",
                    ),
                    rx.text(
                        "Informe as URLs oficiais de download (Google Drive, OneDrive ou nuvem institucional) para cada modelo acadêmico:",
                        size="1",
                        color="#CBD5E1",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    rx.vstack(
                        rx.text("Link do Modelo de Resumo Expandido (.docx)", size="1", weight="bold", color="#CBD5E1"),
                        rx.input(
                            value=EventoState.admin_link_resumo_input,
                            on_change=EventoState.set_admin_link_resumo_input,
                            placeholder="https://drive.google.com/file/d/...",
                            size="2",
                            width="100%",
                        ),
                        rx.text("Link do Slide para Apresentação Oral (15 min)", size="1", weight="bold", color="#CBD5E1"),
                        rx.input(
                            value=EventoState.admin_link_slides_input,
                            on_change=EventoState.set_admin_link_slides_input,
                            placeholder="https://drive.google.com/file/d/...",
                            size="2",
                            width="100%",
                        ),
                        rx.text("Link do Modelo de Pôster / Painel Científico", size="1", weight="bold", color="#CBD5E1"),
                        rx.input(
                            value=EventoState.admin_link_poster_input,
                            on_change=EventoState.set_admin_link_poster_input,
                            placeholder="https://drive.google.com/file/d/...",
                            size="2",
                            width="100%",
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="save", size=15),
                            rx.text("Salvar Links dos Modelos", size="2", weight="bold"),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="cyan",
                        variant="solid",
                        size="2",
                        on_click=EventoState.salvar_links_modelos,
                        style=STYLE_BUTTON_CHIP,
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                padding="1.25rem",
                background="rgba(15, 23, 42, 0.85)",
                border=f"1.5px solid {COLOR_BORDER_CYAN}",
                border_radius="14px",
                width="100%",
                margin_top="1rem",
            ),
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
                color="#CBD5E1",
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
                    on_click=AuthState.abrir_modal_perfil,
                    color_scheme="amber",
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
        conteudo_liberado,
        width="100%",
    )


