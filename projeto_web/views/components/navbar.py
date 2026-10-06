from projeto_web.views.components.modal_perfil import modal_meu_perfil
"""Barra de navegação acadêmica oficial do IV EFAC (View - UI/UX Pro Max).
Pure Deep Cosmic Dark Theme. Adaptável a todas as telas (Desktop, Tablet e Mobile).
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import (
    COLOR_NAVBAR_BG,
    COLOR_BORDER_SUBTLE,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    STYLE_BUTTON_CHIP,
)


def nav_item_secao(texto: str, chave: str, icone: str = "") -> rx.Component:
    """Item do menu superior com indicador visual cósmico de tela ativa e roteamento universal."""
    is_ativa = EventoState.tela_ativa == chave

    return rx.button(
        rx.hstack(
            rx.icon(tag=icone, size=14) if icone else rx.fragment(),
            rx.text(
                texto,
                size="2",
                weight=rx.cond(is_ativa, "bold", "medium"),
            ),
            spacing="1",
            align="center",
        ),
        variant="ghost",
        size="2",
        radius="large",
        padding_x="0.85rem",
        padding_y="0.35rem",
        on_click=EventoState.navegar_para_tela(chave),
        color=rx.cond(
            is_ativa,
            COLOR_CYAN,
            "rgba(226, 232, 240, 0.85)",
        ),
        background=rx.cond(
            is_ativa,
            "rgba(0, 173, 181, 0.15)",
            "transparent",
        ),
        border=rx.cond(
            is_ativa,
            "1px solid rgba(0, 173, 181, 0.35)",
            "1px solid transparent",
        ),
        box_shadow=rx.cond(
            is_ativa,
            "0 0 14px rgba(0, 173, 181, 0.3)",
            "none",
        ),
        _hover={
            "color": COLOR_CYAN_LIGHT,
            "background": "rgba(255, 255, 255, 0.06)",
            "transform": "translateY(-1px)",
        },
        transition="all 0.18s ease",
        style=STYLE_BUTTON_CHIP,
    )


def nav_edital_pulsante(url: str = "/assets/edital_iv_efac_2026.pdf", pronto: bool = False) -> rx.Component:
    """Espaço reservado para o Edital do evento.
    Dedicado exclusivamente a baixar o PDF do evento com regras.
    Mantido desativado até a publicação oficial final do documento.
    """
    if pronto:
        return rx.link(
            rx.badge(
                rx.hstack(
                    rx.icon(tag="file-down", size=13),
                    rx.text("Baixar Edital", size="1", weight="bold"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="cyan",
                variant="solid",
                radius="full",
                padding_x="0.75rem",
                padding_y="0.25rem",
                _hover={"opacity": "1", "transform": "scale(1.05)"},
                style=STYLE_BUTTON_CHIP,
            ),
            href=url,
            download="Edital_IV_EFAC_2026.pdf",
        )

    # Estado desativado preparado para o PDF das regras
    return rx.tooltip(
        rx.box(
            rx.badge(
                rx.hstack(
                    rx.icon(tag="file-text", size=13, color="rgba(255, 255, 255, 0.5)"),
                    rx.text("Edital", size="1", weight="medium", color="rgba(255, 255, 255, 0.7)"),
                    rx.badge("Em Breve", color_scheme="gray", variant="soft", size="1"),
                    spacing="1",
                    align="center",
                ),
                color_scheme="gray",
                variant="surface",
                radius="full",
                padding_x="0.65rem",
                padding_y="0.25rem",
                border="1px dashed rgba(255, 255, 255, 0.2)",
                opacity="0.7",
                cursor="not-allowed",
                style=STYLE_BUTTON_CHIP,
            ),
            id="btn-edital-disabled",
        ),
        content="Edital Oficial com Regras do Evento (Download em breve - aguardando publicação final do PDF)",
    )


def menu_mobile_telas() -> rx.Component:
    """Menu responsivo para telas compactas e tablets (< 1024px)."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon(tag="menu", size=20),
                variant="ghost",
                size="2",
                color="white",
                display=["flex", "flex", "none"],
                aria_label="Abrir Menu de Navegação",
            )
        ),
        rx.menu.content(
            rx.menu.item("Eixos Temáticos", on_click=EventoState.navegar_para_tela("eixos")),
            rx.menu.item("Palestrantes", on_click=EventoState.navegar_para_tela("palestrantes")),
            rx.menu.item("Programação Oficial", on_click=EventoState.navegar_para_tela("programacao")),
            rx.menu.item("Submissões de Trabalhos", on_click=EventoState.navegar_para_tela("submissoes")),
            rx.menu.item("Edital Oficial (PDF em breve)", disabled=True),
            rx.menu.item("Localização", on_click=EventoState.navegar_para_tela("local")),
            rx.menu.item("Sobre o Evento", on_click=EventoState.navegar_para_tela("sobre")),
            rx.menu.separator(),
            rx.menu.item("Garantir Inscrição", on_click=rx.redirect("/inscricao")),
            background="rgba(15, 23, 42, 0.98)",
            border="1px solid rgba(255, 255, 255, 0.12)",
            box_shadow="0 10px 40px rgba(0, 0, 0, 0.6)",
        ),
    )


def navbar() -> rx.Component:
    nav_component = rx.box(
        rx.hstack(
            # Marca / Logo oficial do evento (WhatsApp Image 2026-10-03 at 15.58.16)
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/logo_ivefac.jpeg",
                            alt="Logo Oficial IV EFAC 2026",
                            width="36px",
                            height="36px",
                            border_radius="50%",
                            object_fit="cover",
                            border="1.5px solid #00ADB5",
                            box_shadow="0 0 12px rgba(0, 173, 181, 0.5)",
                        ),
                        display="grid",
                        place_items="center",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.heading(
                                "IV EFAC",
                                size="4",
                                weight="bold",
                                color="white",
                            ),
                            rx.badge("2026", color_scheme="cyan", variant="soft", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        rx.text(
                            "Física & Astronomia • UFCA",
                            size="1",
                            color="var(--gray-9)",
                            style={"white_space": "nowrap"},
                        ),
                        spacing="0",
                        align="start",
                    ),
                    align="center",
                    spacing="2",
                ),
                href="/",
                on_click=EventoState.set_tela("inicio"),
                style=STYLE_BUTTON_CHIP,
            ),
            # Navegação no Topo: Telas Principais (Visível a partir de Desktop / md/lg)
            rx.hstack(
                nav_item_secao("Eixos", "eixos", "orbit"),
                nav_item_secao("Palestrantes", "palestrantes", "users"),
                nav_item_secao("Programação", "programacao", "calendar"),
                nav_item_secao("Submissões", "submissoes", "file-text"),
                nav_edital_pulsante(),
                nav_item_secao("Local", "local", "map-pin"),
                nav_item_secao("Sobre", "sobre", "info"),
                spacing="2",
                align="center",
                display=["none", "none", "flex"],
            ),
            # Acessos (Entrar, Inscreva-se e Menu Mobile)
            rx.hstack(
                rx.cond(
                    EventoState.is_logged_in,
                    rx.hstack(
                        # Botão com nome de acesso direcionando diretamente para a área do usuário
                        rx.tooltip(
                            rx.link(
                                rx.box(
                                    rx.hstack(
                                        rx.box(
                                            rx.cond(
                                                EventoState.user_foto_url != "",
                                                rx.image(
                                                    src=EventoState.user_foto_url,
                                                    width="26px",
                                                    height="26px",
                                                    border_radius="50%",
                                                    object_fit="cover",
                                                    border="1.5px solid #00ADB5",
                                                ),
                                                rx.icon(tag="user", size=15, color="#00ADB5"),
                                            ),
                                            display="grid",
                                            place_items="center",
                                        ),
                                        rx.vstack(
                                            rx.text(
                                                EventoState.user_nome,
                                                size="2",
                                                weight="bold",
                                                color="white",
                                                max_width="140px",
                                                overflow="hidden",
                                                text_overflow="ellipsis",
                                                white_space="nowrap",
                                            ),
                                            rx.hstack(
                                                rx.cond(
                                                    EventoState.is_admin,
                                                    rx.badge("Admin", color_scheme="red", variant="solid", size="1"),
                                                    rx.cond(
                                                        EventoState.is_supervisor,
                                                        rx.badge("Supervisor", color_scheme="violet", variant="solid", size="1"),
                                                        rx.badge("Participante", color_scheme="cyan", variant="surface", size="1"),
                                                    ),
                                                ),
                                                rx.text(EventoState.user_codigo, size="1", color="var(--gray-9)"),
                                                spacing="1",
                                                align="center",
                                            ),
                                            spacing="0",
                                            align="start",
                                        ),
                                        spacing="2",
                                        align="center",
                                    ),
                                    padding="0.3rem 0.75rem",
                                    border_radius="10px",
                                    background="rgba(15, 23, 42, 0.75)",
                                    border="1px solid rgba(0, 173, 181, 0.35)",
                                    box_shadow="0 2px 10px rgba(0, 173, 181, 0.15)",
                                    _hover={
                                        "background": "rgba(0, 173, 181, 0.18)",
                                        "border_color": "#00ADB5",
                                        "transform": "translateY(-1px)",
                                    },
                                    transition="all 0.18s ease",
                                    cursor="pointer",
                                    id="btn-nav-usuario-area",
                                ),
                                href="/inscricao",
                            ),
                            content="Clique para ir diretamente à sua Área de Participante / Painel Administrativo",
                        ),
                        rx.tooltip(
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="user-cog", size=14),
                                    rx.text("Perfil", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                size="1",
                                variant="surface",
                                color_scheme="cyan",
                                on_click=EventoState.abrir_modal_perfil,
                                style=STYLE_BUTTON_CHIP,
                            ),
                            content="Editar perfil, alterar senha e confirmar e-mail",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="log-out", size=14),
                                rx.text("Sair", size="1"),
                                spacing="1",
                                align="center",
                            ),
                            size="1",
                            variant="ghost",
                            color_scheme="red",
                            on_click=EventoState.logout,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.hstack(
                        # Botão Entrar
                        rx.link(
                            rx.button(
                                "Entrar",
                                size="2",
                                variant="outline",
                                color_scheme="cyan",
                                radius="full",
                                padding_x="1rem",
                                border="1.5px solid rgba(0, 173, 181, 0.4)",
                                color="#00ADB5",
                                _hover={
                                    "background": "rgba(0, 173, 181, 0.15)",
                                    "border_color": "#00ADB5",
                                },
                                style=STYLE_BUTTON_CHIP,
                            ),
                            href="/inscricao",
                        ),
                        # Botão Inscreva-se
                        rx.link(
                            rx.button(
                                "Inscreva-se",
                                size="2",
                                variant="solid",
                                color_scheme="indigo",
                                radius="full",
                                padding_x="1.3rem",
                                font_weight="bold",
                                background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                                color="white",
                                box_shadow="0 4px 16px rgba(0, 173, 181, 0.35)",
                                _hover={
                                    "transform": "translateY(-1px)",
                                    "box_shadow": "0 6px 20px rgba(0, 173, 181, 0.5)",
                                },
                                transition="all 0.2s ease",
                                style=STYLE_BUTTON_CHIP,
                            ),
                            href="/inscricao",
                        ),
                        spacing="2",
                        align="center",
                    ),
                ),
                # Menu Mobile
                menu_mobile_telas(),
                spacing="2",
                align="center",
            ),
            justify="between",
            align="center",
            max_width="1320px",
            margin="0 auto",
            padding="0.65rem 1.25rem",
        ),
        position="sticky",
        top="0",
        z_index="100",
        backdrop_filter="blur(16px)",
        background=COLOR_NAVBAR_BG,
        border_bottom=f"1px solid {COLOR_BORDER_SUBTLE}",
        width="100%",
    )

    return rx.fragment(
        nav_component,
        modal_meu_perfil(),
    )
