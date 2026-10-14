"""Seção de Eixos Temáticos do Encontro - Carrossel Pro Max.
Estruturado da mesma forma que Palestrantes Convidados:
- Carrossel rotativo com flechas translúcidas flutuantes sobre os cards.
- Mobile: 1 eixo em destaque com largura total.
- Tablet: 2 eixos em grid responsivo.
- Desktop: 3 eixos simultâneos perfeitamente alinhados e balanceados.
- Indicadores em dots translúcidos interativos.
- Adaptação perfeita de texto (imunidade a zoom, text-wrap balance e overflow-wrap).
"""

import reflex as rx
from projeto_web.controllers.evento_controller import EventoController, EixoTematico
from projeto_web.styles.theme import (
    COLOR_TEXT_PRIMARY,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    COLOR_BORDER_CYAN,
    STYLE_BUTTON_CHIP,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)


class EixosCarouselState(rx.State):
    """Gerenciador do carrossel de Eixos Temáticos com rotação contínua."""
    start_index: int = 0

    def next_slide(self):
        """Avança 1 posição no carrossel."""
        total = len(EventoController.obter_eixos_tematicos())
        if total > 0:
            self.start_index = (self.start_index + 1) % total

    def prev_slide(self):
        """Retorna 1 posição no carrossel."""
        total = len(EventoController.obter_eixos_tematicos())
        if total > 0:
            self.start_index = (self.start_index - 1 + total) % total

    def ir_para_slide(self, index: int):
        self.start_index = index


def card_eixo_hpc(e: EixoTematico) -> rx.Component:
    """Card responsivo de Eixo Temático com design glassmorphic ultra-refinado."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(tag=e.icone, size=24, color=e.cor),
                    padding="0.65rem",
                    border_radius="14px",
                    background=f"{e.cor}22",
                    border=f"1.5px solid {e.cor}55",
                    display="grid",
                    place_items="center",
                ),
                rx.vstack(
                    rx.badge(f"Eixo Temático 0{e.numero}", color_scheme="cyan", variant="surface", size="2", style=STYLE_BUTTON_CHIP),
                    rx.heading(
                        e.titulo,
                        size="4",
                        weight="bold",
                        color=COLOR_TEXT_PRIMARY,
                        style=STYLE_HEADING_RESPONSIVE,
                        text_wrap="balance",
                        overflow_wrap="break-word",
                    ),
                    spacing="1",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.text(
                e.subtitulo,
                size="2",
                weight="medium",
                color=COLOR_CYAN_LIGHT,
                style=STYLE_HEADING_RESPONSIVE,
                text_wrap="balance",
            ),
            rx.text(
                e.descricao,
                size="2",
                color="#E2E8F0",
                line_height="1.6",
                style=STYLE_TEXT_RESPONSIVE,
                text_wrap="balance",
                overflow_wrap="break-word",
                flex="1",
            ),
            rx.divider(color_scheme="gray", opacity="0.15"),
            rx.hstack(
                *[rx.badge(t, size="1", variant="outline", style=STYLE_BUTTON_CHIP) for t in e.tags],
                spacing="2",
                wrap="wrap",
                width="100%",
            ),
            spacing="3",
            align="start",
            justify="between",
            width="100%",
            height="100%",
        ),
        padding="1.6rem",
        border_radius="18px",
        min_height="330px",
        height="100%",
        background=COLOR_SURFACE_GLASS,
        backdrop_filter="blur(18px)",
        border=f"1.5px solid {COLOR_BORDER_CYAN}",
        box_shadow="0 10px 32px rgba(0, 0, 0, 0.4)",
        _hover={
            "transform": "translateY(-4px)",
            "border_color": e.cor,
            "box_shadow": f"0 14px 40px {e.cor}35",
        },
        transition="all 0.25s ease",
        width="100%",
    )


def _eixo_carousel_slot(slot_offset: int) -> rx.Component:
    """Retorna o card do eixo temático no slot relativo ao índice atual."""
    eixos = EventoController.obter_eixos_tematicos()
    total = len(eixos)
    slot_idx = (EixosCarouselState.start_index + slot_offset) % total

    return rx.match(
        slot_idx,
        *[(i, card_eixo_hpc(e)) for i, e in enumerate(eixos)],
        card_eixo_hpc(eixos[0]),
    )


def tela_eixos() -> rx.Component:
    """Seção de Eixos Temáticos com Carrossel interativo, flechas translúcidas flutuantes e alta adaptabilidade."""
    eixos = EventoController.obter_eixos_tematicos()
    total = len(eixos)

    # Botão de flecha translúcida anterior (esquerda)
    btn_prev_overlay = rx.box(
        rx.button(
            rx.icon(tag="chevron-left", size=24, color="white"),
            size="3",
            variant="ghost",
            border_radius="full",
            width="44px",
            height="44px",
            padding="0",
            display="grid",
            place_items="center",
            background="rgba(6, 8, 20, 0.75)",
            backdrop_filter="blur(14px)",
            border="1.5px solid rgba(0, 173, 181, 0.5)",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 173, 181, 0.35)",
            _hover={
                "background": "rgba(0, 173, 181, 0.35)",
                "border_color": "#00ADB5",
                "transform": "scale(1.12)",
                "box_shadow": "0 6px 25px rgba(0, 173, 181, 0.6)",
            },
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            on_click=EixosCarouselState.prev_slide,
            cursor="pointer",
            id="btn-eixos-carousel-prev",
        ),
        position="absolute",
        left=rx.breakpoints(initial="-8px", sm="4px", md="-22px"),
        top="50%",
        transform="translateY(-50%)",
        z_index="20",
    )

    # Botão de flecha translúcida seguinte (direita)
    btn_next_overlay = rx.box(
        rx.button(
            rx.icon(tag="chevron-right", size=24, color="white"),
            size="3",
            variant="ghost",
            border_radius="full",
            width="44px",
            height="44px",
            padding="0",
            display="grid",
            place_items="center",
            background="rgba(6, 8, 20, 0.75)",
            backdrop_filter="blur(14px)",
            border="1.5px solid rgba(0, 173, 181, 0.5)",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 173, 181, 0.35)",
            _hover={
                "background": "rgba(0, 173, 181, 0.35)",
                "border_color": "#00ADB5",
                "transform": "scale(1.12)",
                "box_shadow": "0 6px 25px rgba(0, 173, 181, 0.6)",
            },
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            on_click=EixosCarouselState.next_slide,
            cursor="pointer",
            id="btn-eixos-carousel-next",
        ),
        position="absolute",
        right=rx.breakpoints(initial="-8px", sm="4px", md="-22px"),
        top="50%",
        transform="translateY(-50%)",
        z_index="20",
    )

    return rx.box(
        rx.vstack(
            rx.heading(
                "Eixos Temáticos do Encontro",
                size=rx.breakpoints(initial="6", sm="7", md="8"),
                weight="bold",
                color=COLOR_TEXT_PRIMARY,
                text_align="center",
                style=STYLE_HEADING_RESPONSIVE,
            ),
            rx.text(
                "Estrutura temática para apresentação de artigos, resumos expandidos e mesas de debate.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="#E2E8F0",
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
                max_width="720px",
            ),

            # Container com flechas flutuantes e slots responsivos
            rx.box(
                btn_prev_overlay,
                btn_next_overlay,
                # Botão invisível do timer automático de 15 segundos
                rx.button(
                    "auto_next_eixos",
                    id="btn-eixos-carousel-next-auto",
                    display="none",
                    on_click=EixosCarouselState.next_slide,
                ),
                rx.box(
                    # Mobile: 1 eixo em destaque
                    rx.box(
                        _eixo_carousel_slot(0),
                        width="100%",
                        max_width="440px",
                        margin="0 auto",
                        display=rx.breakpoints(initial="block", sm="none"),
                    ),
                    # Tablet: 2 eixos
                    rx.grid(
                        _eixo_carousel_slot(0),
                        _eixo_carousel_slot(1),
                        columns="2",
                        spacing="4",
                        width="100%",
                        display=rx.breakpoints(initial="none", sm="grid", md="none"),
                    ),
                    # Desktop: 3 eixos simultâneos
                    rx.grid(
                        _eixo_carousel_slot(0),
                        _eixo_carousel_slot(1),
                        _eixo_carousel_slot(2),
                        columns="3",
                        spacing="4",
                        width="100%",
                        display=rx.breakpoints(initial="none", md="grid"),
                    ),
                    width="100%",
                ),
                position="relative",
                width="100%",
                max_width="1280px",
                margin_top="1rem",
                padding_x=rx.breakpoints(initial="1.5rem", sm="1.8rem", md="0"),
            ),

            # Indicadores / Dots de navegação
            rx.hstack(
                *[
                    rx.box(
                        width=rx.cond(EixosCarouselState.start_index == i, "24px", "8px"),
                        height="8px",
                        border_radius="full",
                        background=rx.cond(EixosCarouselState.start_index == i, COLOR_CYAN, "rgba(255, 255, 255, 0.2)"),
                        cursor="pointer",
                        on_click=EixosCarouselState.ir_para_slide(i),
                        transition="all 0.25s ease",
                    )
                    for i in range(total)
                ],
                spacing="2",
                align="center",
                justify="center",
                margin_top="1rem",
            ),

            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        # Script do timer de 15 segundos (mesmo intervalo de transição dos palestrantes)
        rx.script(
            """
            (function() {
                if (window.__efac_eixos_carousel_timer) {
                    clearInterval(window.__efac_eixos_carousel_timer);
                }
                window.__efac_eixos_carousel_timer = setInterval(function() {
                    var btn = document.getElementById('btn-eixos-carousel-next-auto');
                    if (btn) {
                        btn.click();
                    }
                }, 15000);
            })();
            """
        ),
        id="eixos",
        width="100%",
    )
