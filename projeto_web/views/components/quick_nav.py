"""Menu de Acesso Rápido Flutuante (Quick Nav Corner Dock) - IV EFAC 2026.
Permite salto suave imediato entre todas as seções da Landing Page única.
"""

import reflex as rx
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
)


def _quick_nav_btn(icone: str, rotulo: str, href_target: str) -> rx.Component:
    """Botão individual do menu rápido flutuante com tooltip e animação suave."""
    return rx.tooltip(
        rx.link(
            rx.box(
                rx.icon(tag=icone, size=18, color=COLOR_CYAN),
                padding="0.6rem",
                border_radius="12px",
                background="rgba(15, 23, 42, 0.75)",
                backdrop_filter="blur(14px)",
                border=f"1px solid {COLOR_BORDER_CYAN}",
                box_shadow="0 4px 16px rgba(0, 0, 0, 0.4)",
                display="grid",
                place_items="center",
                transition="all 0.25s cubic-bezier(0.4, 0, 0.2, 1)",
                _hover={
                    "background": "rgba(0, 173, 181, 0.22)",
                    "border_color": COLOR_CYAN,
                    "transform": "scale(1.12) translateX(-3px)",
                    "box_shadow": "0 6px 20px rgba(0, 173, 181, 0.4)",
                },
                cursor="pointer",
            ),
            href=href_target,
        ),
        content=rotulo,
        side="left",
    )


def quick_nav() -> rx.Component:
    """Dock flutuante lateral/canto inferior direito com navegação instantânea."""
    return rx.box(
        rx.vstack(
            _quick_nav_btn("home", "Início / Hero", "#inicio"),
            _quick_nav_btn("info", "Sobre o IV EFAC", "#sobre"),
            _quick_nav_btn("orbit", "Eixos Temáticos", "#eixos"),
            _quick_nav_btn("users", "Palestrantes (Keynotes)", "#palestrantes"),
            _quick_nav_btn("calendar", "Grade & Programação", "#programacao"),
            _quick_nav_btn("map-pin", "Localização & Parcerias", "#local"),
            _quick_nav_btn("ticket", "Área de Inscrição", "/inscricao"),
            spacing="2",
            align="center",
        ),
        position="fixed",
        right="1.2rem",
        bottom="1.5rem",
        z_index="999",
        display=rx.breakpoints(initial="none", sm="flex"),
        pointer_events="auto",
    )
