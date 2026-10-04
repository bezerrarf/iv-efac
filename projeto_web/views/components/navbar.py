"""Barra de navegação acadêmica oficial do IV EFAC (View).
Permite alternar entre as seções/telas diretamente pelos itens do topo com feedback ativo.
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState


def nav_item_secao(texto: str, chave: str, icone: str = "") -> rx.Component:
    """Item do menu superior com indicador visual de tela ativa."""
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
            rx.color_mode_cond(light="#103460", dark="#00ADB5"),
            rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
        ),
        background=rx.cond(
            is_ativa,
            rx.color_mode_cond(light="rgba(16, 52, 96, 0.08)", dark="rgba(0, 173, 181, 0.15)"),
            "transparent",
        ),
        border=rx.cond(
            is_ativa,
            rx.color_mode_cond(light="1px solid rgba(16, 52, 96, 0.2)", dark="1px solid rgba(0, 173, 181, 0.3)"),
            "1px solid transparent",
        ),
        box_shadow=rx.cond(
            is_ativa,
            rx.color_mode_cond(light="0 2px 8px rgba(16, 52, 96, 0.08)", dark="0 0 12px rgba(0, 173, 181, 0.25)"),
            "none",
        ),
        _hover={
            "color": rx.color_mode_cond(light="#103460", dark="#38bdf8"),
            "background": rx.color_mode_cond(light="rgba(0, 0, 0, 0.04)", dark="rgba(255, 255, 255, 0.06)"),
            "transform": "translateY(-1px)",
        },
        transition="all 0.18s ease",
    )


def nav_edital_pulsante(url: str = "/cronograma") -> rx.Component:
    """Link do Edital com efeito pulsante contínuo."""
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
            },
            _hover={"opacity": "1", "transform": "scale(1.05)"},
        ),
        href=url,
    )


def botao_alternar_tema() -> rx.Component:
    """Botão moderno de alternância entre Buraco Negro (Escuro) e Anã Branca (Claro)."""
    return rx.tooltip(
        rx.button(
            rx.color_mode_cond(
                light=rx.icon(tag="moon", size=18, color="#1e293b"),
                dark=rx.icon(tag="sun", size=18, color="#facc15"),
            ),
            variant="ghost",
            size="2",
            radius="full",
            on_click=rx.toggle_color_mode,
            _hover={
                "background": rx.color_mode_cond(
                    light="rgba(0, 0, 0, 0.05)",
                    dark="rgba(255, 255, 255, 0.1)",
                )
            },
            aria_label="Alternar Tema: Buraco Negro / Anã Branca",
        ),
        content=rx.color_mode_cond(
            light="Mudar para Buraco Negro (Tema Escuro)",
            dark="Mudar para Anã Branca (Tema Claro)",
        ),
    )


def menu_mobile_telas() -> rx.Component:
    """Menu responsivo para dispositivos móveis."""
    return rx.menu.root(
        rx.menu.trigger(
            rx.button(
                rx.icon(tag="menu", size=20),
                variant="ghost",
                size="2",
                color=rx.color_mode_cond(light="#103460", dark="white"),
                display=["flex", "flex", "none"],
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
            background=rx.color_mode_cond(light="#ffffff", dark="rgba(15, 23, 42, 0.98)"),
            border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.1)"),
        ),
    )


def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            # Marca / Logo oficial do evento (ao clicar retorna ao Início)
            rx.link(
                rx.hstack(
                    rx.box(
                        rx.image(
                            src="/logo_ivefac.jpeg",
                            width="32px",
                            height="32px",
                            border_radius="50%",
                            object_fit="cover",
                            border=rx.color_mode_cond(
                                light="2px solid #103460",
                                dark="2px solid #00ADB5",
                            ),
                            box_shadow=rx.color_mode_cond(
                                light="0 0 10px rgba(16, 52, 96, 0.3)",
                                dark="0 0 12px rgba(0, 173, 181, 0.6)",
                            ),
                        ),
                        position="relative",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.heading(
                                "IV EFAC",
                                size="4",
                                weight="bold",
                                color=rx.color_mode_cond(light="#103460", dark="white"),
                            ),
                            rx.badge("2026", color_scheme="cyan", variant="soft", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        rx.text(
                            "Física & Astronomia • UFCA",
                            size="1",
                            color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)"),
                        ),
                        spacing="0",
                        align="start",
                    ),
                    align="center",
                    spacing="2",
                ),
                href="/",
                on_click=lambda: EventoState.set_tela("inicio"),
            ),
            # Navegação no Topo: Eixos, Palestrantes, Programação, Submissões, Edital, Local e Sobre (último item)
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
            # Acessos (Entrar, Inscreva-se, Alternador de Tema e Menu Mobile)
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
                                border=rx.color_mode_cond(
                                    light="1.5px solid #cbd5e1",
                                    dark="1.5px solid rgba(0, 173, 181, 0.4)",
                                ),
                                color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                                _hover={
                                    "background": rx.color_mode_cond(
                                        light="#f1f5f9",
                                        dark="rgba(0, 173, 181, 0.12)",
                                    ),
                                },
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
                                padding_x="1.4rem",
                                font_weight="bold",
                                background="#103460",
                                color="white",
                                box_shadow="0 4px 15px rgba(16, 52, 96, 0.3)",
                                _hover={"transform": "translateY(-1px)", "background": "#16457e"},
                                transition="all 0.2s ease",
                            ),
                            href="/inscricao",
                        ),
                        spacing="2",
                        align="center",
                    ),
                ),
                # Alternador de Tema Cósmico
                botao_alternar_tema(),
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
        background=rx.color_mode_cond(
            light="rgba(255, 255, 255, 0.92)",
            dark="rgba(6, 8, 20, 0.92)",
        ),
        border_bottom=rx.color_mode_cond(
            light="1px solid #e2e8f0",
            dark="1px solid rgba(255, 255, 255, 0.08)",
        ),
        width="100%",
    )
