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
    """Item do menu superior com indicador visual cósmico de tela ativa."""
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
        on_click=lambda: EventoState.set_tela(chave),
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


def nav_edital_pulsante(url: str = "/cronograma") -> rx.Component:
    """Link do Edital com efeito pulsante contínuo e prevenção de quebra."""
    return rx.link(
        rx.badge(
            rx.hstack(
                rx.icon(tag="file-text", size=13),
                rx.text("Edital", size="1", weight="bold"),
                spacing="1",
                align="center",
            ),
            color_scheme="cyan",
            variant="solid",
            radius="full",
            padding_x="0.75rem",
            padding_y="0.25rem",
            style={
                "@keyframes piscaEdital": {
                    "0%, 100%": {"opacity": "1", "transform": "scale(1)"},
                    "50%": {"opacity": "0.6", "transform": "scale(0.96)"},
                },
                "animation": "piscaEdital 1.8s ease-in-out infinite",
                **STYLE_BUTTON_CHIP,
            },
            _hover={"opacity": "1", "transform": "scale(1.05)"},
        ),
        href=url,
        style=STYLE_BUTTON_CHIP,
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
            rx.menu.item("Eixos Temáticos", on_click=lambda: EventoState.set_tela("eixos")),
            rx.menu.item("Palestrantes", on_click=lambda: EventoState.set_tela("palestrantes")),
            rx.menu.item("Programação Oficial", on_click=lambda: EventoState.set_tela("programacao")),
            rx.menu.item("Submissões de Trabalhos", on_click=lambda: EventoState.set_tela("submissoes")),
            rx.menu.item("Edital Oficial", on_click=rx.redirect("/cronograma")),
            rx.menu.item("Localização", on_click=lambda: EventoState.set_tela("local")),
            rx.menu.item("Sobre o Evento", on_click=lambda: EventoState.set_tela("sobre")),
            rx.menu.separator(),
            rx.menu.item("Garantir Inscrição", on_click=rx.redirect("/inscricao")),
            background="rgba(15, 23, 42, 0.98)",
            border="1px solid rgba(255, 255, 255, 0.12)",
            box_shadow="0 10px 40px rgba(0, 0, 0, 0.6)",
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Marca / Logo oficial do evento
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.box(
                            width="30px",
                            height="30px",
                            border_radius="50%",
                            border="2px solid #00ADB5",
                            box_shadow="0 0 14px rgba(0, 173, 181, 0.6)",
                            display="grid",
                            place_items="center",
                            background="radial-gradient(circle, #00ADB5 20%, transparent 75%)",
                        ),
                        position="relative",
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
                on_click=lambda: EventoState.set_tela("inicio"),
                style=STYLE_BUTTON_CHIP,
            ),
            # Navegação no Topo: Telas Principais (Visível a partir de Desktop / md/lg)
            rx.hstack(
                nav_item_secao("Eixos", "eixos", "orbit"),
                nav_item_secao("Palestrantes", "palestrantes", "users"),
                nav_item_secao("Programação", "programacao", "calendar"),
                nav_item_secao("Submissões", "submissoes", "file-text"),
                nav_edital_pulsante("/cronograma"),
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
                        rx.badge(
                            rx.hstack(
                                rx.icon(tag="circle-check", size=14),
                                rx.text(EventoState.user_codigo, size="1"),
                                spacing="1",
                                align="center",
                            ),
                            color_scheme="green",
                            variant="surface",
                        ),
                        rx.button(
                            "Sair",
                            size="2",
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
