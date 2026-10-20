"""Seção de Palestrantes Convidados (Keynotes) - Carrossel Pro Max.
Melhorias Solicitadas:
- Somente o título superior 'Palestrantes Convidados'.
- Remoção do texto 'Carrossel Automático (15s) • 4 banners visíveis'.
- Ícones de flechas translúcidas posicionadas diretamente sobre os banners.
- Mobile otimizado: 1 banner em destaque por vez no mobile (em vez de 4 cards empilhados),
  avançando de 1 em 1 a cada 15s com flechas flutuantes.
- Desktop: 4 banners simultâneos perfeitamente alinhados.
- Expansão interativa: ao clicar no banner, expande os detalhes; ao clicar novamente, retorna.
"""

import reflex as rx
from projeto_web.controllers.evento_controller import EventoController, Palestrante
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


class PalestrantesCarouselState(rx.State):
    """Gerenciador do carrossel: índice inicial e palestrante expandido."""
    start_index: int = 0
    expanded_nome: str = ""

    def next_slide(self):
        """Avança 1 posição."""
        total = len(EventoController.obter_palestrantes())
        if total > 0:
            self.start_index = (self.start_index + 1) % total

    def prev_slide(self):
        """Volta 1 posição."""
        total = len(EventoController.obter_palestrantes())
        if total > 0:
            self.start_index = (self.start_index - 1 + total) % total

    def toggle_expand(self, nome: str):
        """Expande / recolhe banner."""
        if self.expanded_nome == nome:
            self.expanded_nome = ""
        else:
            self.expanded_nome = nome

    def close_expand(self):
        """Fecha expansão."""
        self.expanded_nome = ""


def _palestrante_card_banner(p: Palestrante) -> rx.Component:
    """Card de banner de palestrante com imagem e dados essenciais."""
    return rx.card(
        rx.vstack(
            # Foto/Banner oficial em destaque
            rx.box(
                rx.image(
                    src=p.foto,
                    alt=f"Foto oficial de {p.nome}",
                    width="100%",
                    height=rx.breakpoints(initial="230px", sm="210px", md="205px"),
                    object_fit="cover",
                    object_position="center top",
                    border_radius="10px",
                    filter="drop-shadow(0 4px 10px rgba(0, 0, 0, 0.4))",
                    _hover={"transform": "scale(1.025)"},
                    transition="transform 0.3s ease",
                ),
                rx.badge(
                    "Clique para expandir",
                    size="1",
                    variant="solid",
                    color_scheme="cyan",
                    position="absolute",
                    bottom="8px",
                    right="8px",
                    style=STYLE_BUTTON_CHIP,
                ),
                width="100%",
                height=rx.breakpoints(initial="230px", sm="210px", md="205px"),
                overflow="hidden",
                border_radius="10px",
                border=f"1.5px solid {COLOR_BORDER_CYAN}",
                position="relative",
                background="rgba(15, 23, 42, 0.8)",
            ),
            # Nome e Titulação
            rx.heading(
                p.nome,
                size="3",
                weight="bold",
                text_align="center",
                color=COLOR_TEXT_PRIMARY,
                style=STYLE_HEADING_RESPONSIVE,
                margin_top="0.3rem",
            ),
            rx.badge(
                p.instituicao,
                size="1",
                variant="soft",
                color_scheme="indigo",
                style=STYLE_BUTTON_CHIP,
            ),
            rx.text(
                p.cargo,
                size="1",
                color=COLOR_CYAN_LIGHT,
                text_align="center",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            rx.text(
                p.especialidade,
                size="1",
                color="#CBD5E1",
                text_align="center",
                line_height="1.4",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            # Tópico da Apresentação
            rx.cond(
                p.topico != "",
                rx.box(
                    rx.text(
                        p.topico,
                        size="1",
                        weight="medium",
                        color=COLOR_CYAN,
                        text_align="center",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    padding="0.35rem 0.55rem",
                    border_radius="8px",
                    background="rgba(0, 173, 181, 0.12)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    width="100%",
                    margin_top="0.2rem",
                ),
                rx.fragment(),
            ),
            justify="between",
            align="center",
            width="100%",
            height="100%",
            spacing="2",
        ),
        padding="1rem",
        width="100%",
        height="100%",
        border_radius="16px",
        background=COLOR_SURFACE_GLASS,
        backdrop_filter="blur(16px)",
        border=f"1px solid {COLOR_BORDER_CYAN}",
        box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
        cursor="pointer",
        _hover={
            "transform": "translateY(-3px)",
            "border_color": COLOR_CYAN,
            "box_shadow": "0 10px 32px rgba(0, 173, 181, 0.3)",
        },
        transition="all 0.25s ease",
        on_click=PalestrantesCarouselState.toggle_expand(p.nome),
    )


def _carousel_slot(slot_offset: int) -> rx.Component:
    """Retorna o componente do palestrante correspondente ao slot dinâmico."""
    palestrantes = EventoController.obter_palestrantes()
    total = len(palestrantes)
    slot_idx = (PalestrantesCarouselState.start_index + slot_offset) % total

    return rx.match(
        slot_idx,
        *[(i, _palestrante_card_banner(p)) for i, p in enumerate(palestrantes)],
        _palestrante_card_banner(palestrantes[0]),
    )


def _modal_banner_expandido() -> rx.Component:
    """Modal de alta resolução ao clicar em qualquer banner."""
    palestrantes = EventoController.obter_palestrantes()

    return rx.cond(
        PalestrantesCarouselState.expanded_nome != "",
        rx.box(
            rx.box(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.badge("Banner Detalhado do Convidado", color_scheme="cyan", size="2"),
                            rx.spacer(),
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="minimize-2", size=16),
                                    rx.text("Fechar", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                size="1",
                                color_scheme="red",
                                variant="surface",
                                on_click=PalestrantesCarouselState.close_expand,
                                cursor="pointer",
                            ),
                            width="100%",
                            align="center",
                        ),
                        # Detalhes do palestrante
                        rx.box(
                            *[
                                rx.cond(
                                    PalestrantesCarouselState.expanded_nome == p.nome,
                                    rx.grid(
                                        rx.box(
                                            rx.image(
                                                src=p.foto,
                                                alt=f"Banner oficial {p.nome}",
                                                width="100%",
                                                max_height="400px",
                                                object_fit="contain",
                                                border_radius="14px",
                                                border=f"2px solid {COLOR_BORDER_CYAN}",
                                                box_shadow="0 8px 30px rgba(0, 173, 181, 0.4)",
                                                background="rgba(6, 8, 20, 0.9)",
                                            ),
                                            width="100%",
                                            display="grid",
                                            place_items="center",
                                        ),
                                        rx.vstack(
                                            rx.badge(p.instituicao, color_scheme="indigo", size="2"),
                                            rx.heading(p.nome, size="6", weight="bold", color="white"),
                                            rx.text(p.cargo, size="3", color=COLOR_CYAN_LIGHT, weight="medium"),
                                            rx.divider(color_scheme="gray", opacity="0.2"),
                                            rx.vstack(
                                                rx.text("Linha de Pesquisa & Especialidade:", size="2", weight="bold", color=COLOR_CYAN),
                                                rx.text(p.especialidade, size="2", color="#E2E8F0", line_height="1.6"),
                                                spacing="1",
                                                align="start",
                                            ),
                                            rx.cond(
                                                p.topico != "",
                                                rx.box(
                                                    rx.text("Conferência Magna / Apresentação:", size="1", weight="bold", color=COLOR_CYAN_LIGHT),
                                                    rx.text(p.topico, size="3", weight="bold", color="white", margin_top="0.2rem"),
                                                    padding="0.8rem 1.2rem",
                                                    border_radius="10px",
                                                    background="rgba(0, 173, 181, 0.15)",
                                                    border=f"1px solid {COLOR_BORDER_CYAN}",
                                                    width="100%",
                                                ),
                                                rx.fragment(),
                                            ),
                                            rx.button(
                                                "Clique para recolher e voltar ao carrossel",
                                                size="2",
                                                variant="outline",
                                                color_scheme="cyan",
                                                radius="full",
                                                on_click=PalestrantesCarouselState.close_expand,
                                                margin_top="1rem",
                                                width="100%",
                                            ),
                                            spacing="3",
                                            align="start",
                                            justify="center",
                                            height="100%",
                                        ),
                                        columns=rx.breakpoints(initial="1", md="2"),
                                        spacing="4",
                                        width="100%",
                                    ),
                                    rx.fragment(),
                                )
                                for p in palestrantes
                            ],
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                    padding="1.8rem",
                    border_radius="20px",
                    background="rgba(11, 19, 43, 0.96)",
                    backdrop_filter="blur(24px)",
                    border=f"2px solid {COLOR_CYAN}",
                    box_shadow="0 16px 60px rgba(0, 173, 181, 0.5)",
                    max_width="880px",
                    width="95%",
                    margin="0 auto",
                    on_click=PalestrantesCarouselState.close_expand,
                    cursor="pointer",
                ),
                display="grid",
                place_items="center",
                width="100%",
                height="100%",
                padding="1rem",
            ),
            position="fixed",
            inset="0",
            z_index="999",
            background="rgba(6, 8, 20, 0.85)",
            backdrop_filter="blur(12px)",
            display="grid",
            place_items="center",
            on_click=PalestrantesCarouselState.close_expand,
        ),
        rx.fragment(),
    )


def tela_palestrantes() -> rx.Component:
    """Seção de Palestrantes Convidados com flechas translúcidas flutuantes sobre o banner
    e apresentação responsiva (1 no mobile, 2 no tablet e 4 no desktop)."""
    palestrantes = EventoController.obter_palestrantes()
    total = len(palestrantes)

    # Botão de flecha translúcida anterior (sobreposto à esquerda)
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
            background="rgba(6, 8, 20, 0.7)",
            backdrop_filter="blur(12px)",
            border="1.5px solid rgba(0, 173, 181, 0.5)",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 173, 181, 0.35)",
            _hover={
                "background": "rgba(0, 173, 181, 0.35)",
                "border_color": "#00ADB5",
                "transform": "scale(1.12)",
                "box_shadow": "0 6px 25px rgba(0, 173, 181, 0.6)",
            },
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            on_click=PalestrantesCarouselState.prev_slide,
            cursor="pointer",
            id="btn-carousel-prev-overlay",
        ),
        position="absolute",
        left=rx.breakpoints(initial="-8px", sm="4px", md="-20px"),
        top="50%",
        transform="translateY(-50%)",
        z_index="20",
    )

    # Botão de flecha translúcida seguinte (sobreposto à direita)
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
            background="rgba(6, 8, 20, 0.7)",
            backdrop_filter="blur(12px)",
            border="1.5px solid rgba(0, 173, 181, 0.5)",
            box_shadow="0 4px 20px rgba(0, 0, 0, 0.6), 0 0 15px rgba(0, 173, 181, 0.35)",
            _hover={
                "background": "rgba(0, 173, 181, 0.35)",
                "border_color": "#00ADB5",
                "transform": "scale(1.12)",
                "box_shadow": "0 6px 25px rgba(0, 173, 181, 0.6)",
            },
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            on_click=PalestrantesCarouselState.next_slide,
            cursor="pointer",
            id="btn-carousel-next-overlay",
        ),
        position="absolute",
        right=rx.breakpoints(initial="-8px", sm="4px", md="-20px"),
        top="50%",
        transform="translateY(-50%)",
        z_index="20",
    )

    return rx.box(
        rx.vstack(
            # SOMENTE o título superior
            rx.heading(
                "Palestrantes Convidados",
                size=rx.breakpoints(initial="6", sm="7", md="8"),
                weight="bold",
                color=COLOR_TEXT_PRIMARY,
                text_align="center",
                style=STYLE_HEADING_RESPONSIVE,
                margin_bottom="1rem",
            ),

            # Container relativo com as flechas translúcidas flutuantes sobre o carrossel
            rx.box(
                btn_prev_overlay,
                btn_next_overlay,
                # Botão invisível do timer de 15s
                rx.button(
                    "auto_next",
                    id="btn-carousel-next-auto",
                    display="none",
                    on_click=PalestrantesCarouselState.next_slide,
                ),
                # Grid Adaptativo:
                # No mobile: Slot 0 visível com largura total (1 banner destacado)
                # No tablet: Slots 0 e 1 visíveis (2 banners)
                # No desktop: Slots 0, 1, 2 e 3 visíveis (4 banners)
                rx.box(
                    # Visualização Mobile: 1 banner em destaque
                    rx.box(
                        _carousel_slot(0),
                        width="100%",
                        max_width="440px",
                        margin="0 auto",
                        display=rx.breakpoints(initial="block", sm="none"),
                    ),
                    # Visualização Tablet: 2 banners
                    rx.grid(
                        _carousel_slot(0),
                        _carousel_slot(1),
                        columns="2",
                        spacing="4",
                        width="100%",
                        display=rx.breakpoints(initial="none", sm="grid", md="none"),
                    ),
                    # Visualização Desktop: 4 banners simultâneos
                    rx.grid(
                        _carousel_slot(0),
                        _carousel_slot(1),
                        _carousel_slot(2),
                        _carousel_slot(3),
                        columns="4",
                        spacing="4",
                        width="100%",
                        display=rx.breakpoints(initial="none", md="grid"),
                    ),
                    width="100%",
                ),
                position="relative",
                width="100%",
                max_width="1280px",
                padding_x=rx.breakpoints(initial="1.5rem", sm="1.8rem", md="0"),
            ),

            # Chamadas de Ação
            rx.hstack(
                rx.link(
                    rx.button(
                        rx.hstack(
                            rx.text("Conferir a Grade Horária do Simpósio"),
                            rx.icon(tag="arrow-down", size=16),
                            spacing="1",
                            align="center",
                        ),
                        size="3",
                        radius="full",
                        background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                        color="white",
                        box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                        _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.55)"},
                        style=STYLE_BUTTON_CHIP,
                    ),
                    href="#programacao",
                ),
                rx.link(
                    rx.button(
                        "Garantir Vaga no Evento",
                        size="3",
                        variant="outline",
                        color_scheme="cyan",
                        radius="full",
                        style=STYLE_BUTTON_CHIP,
                    ),
                    href="/inscricao",
                ),
                spacing="3",
                margin_top="1.5rem",
                wrap="wrap",
                justify="center",
            ),

            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="2rem",
        ),
        # Visualização expandida
        _modal_banner_expandido(),
        # Script do timer de 15 segundos
        rx.script(
            """
            (function() {
                if (window.__efac_carousel_timer) {
                    clearInterval(window.__efac_carousel_timer);
                }
                window.__efac_carousel_timer = setInterval(function() {
                    var btn = document.getElementById('btn-carousel-next-auto');
                    if (btn) {
                        btn.click();
                    }
                }, 15000);
            })();
            """
        ),
        id="palestrantes",
        width="100%",
    )
