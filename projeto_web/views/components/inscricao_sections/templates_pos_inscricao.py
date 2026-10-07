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
                    on_click=AuthState.abrir_modal_perfil,
                    color_scheme="amber",
                    size="2",
                    cursor="pointer",
                ),
                rx.button(
                    rx.icon(tag="check", size=16),
                    "Verificação Direta Instantânea",
                    on_click=AuthState.confirmar_email_direto,
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
            AuthState.email_confirmado,
            conteudo_liberado,
            aviso_bloqueio_email,
        ),
        width="100%",
    )


