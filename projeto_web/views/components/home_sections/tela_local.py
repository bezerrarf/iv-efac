"""Seção de Localização e Conectividade Acadêmica do IV EFAC (Landing Page).
Contém:
1. Card informativo com endereço do Campus Brejo Santo - UFCA.
2. Mapa interativo com link direto para o Google Maps.
3. Relação de logos e chips oficiais das faculdades e instituições de fomento do evento.
"""

import reflex as rx
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


def _instituicao_link_chip(nome: str, papel: str, url_home: str, logo_file: str) -> rx.Component:
    """Chip interativo com logotipo oficial e link externo para a página da instituição."""
    return rx.link(
        rx.box(
            rx.hstack(
                rx.image(
                    src=f"/logos/{logo_file}",
                    alt=f"Logo oficial de {nome}",
                    height="28px",
                    max_width="70px",
                    object_fit="contain",
                    filter="brightness(1.1) drop-shadow(0 2px 4px rgba(0, 0, 0, 0.4))",
                ),
                rx.vstack(
                    rx.text(nome, size="2", weight="bold", color=COLOR_TEXT_PRIMARY),
                    rx.text(papel, size="1", color="#CBD5E1"),
                    spacing="0",
                    align="start",
                ),
                rx.icon(tag="external-link", size=12, color=COLOR_CYAN_LIGHT),
                spacing="2",
                align="center",
            ),
            padding="0.55rem 0.95rem",
            border_radius="12px",
            background="rgba(15, 23, 42, 0.8)",
            backdrop_filter="blur(14px)",
            border=f"1px solid {COLOR_BORDER_CYAN}",
            box_shadow="0 4px 14px rgba(0, 0, 0, 0.3)",
            _hover={
                "border_color": COLOR_CYAN,
                "background": "rgba(0, 173, 181, 0.2)",
                "transform": "translateY(-2px)",
                "box_shadow": "0 6px 20px rgba(0, 173, 181, 0.35)",
            },
            transition="all 0.2s cubic-bezier(0.4, 0, 0.2, 1)",
            cursor="pointer",
        ),
        href=url_home,
        is_external=True,
        style=STYLE_BUTTON_CHIP,
    )


def tela_local() -> rx.Component:
    """Apresentação de Localização com mapa e grade com os logos oficiais das instituições parceiras."""
    maps_url = "https://maps.google.com/?q=Universidade+Federal+do+Cariri+Campus+Brejo+Santo"

    return rx.box(
        rx.vstack(
            rx.heading(
                "Localização & Polo Acadêmico",
                size=rx.breakpoints(initial="6", sm="7", md="8"),
                weight="bold",
                color=COLOR_TEXT_PRIMARY,
                text_align="center",
                style=STYLE_HEADING_RESPONSIVE,
            ),
            rx.text(
                "O IV EFAC será realizado presencialmente nas instalações de vanguarda do Campus Brejo Santo da UFCA.",
                size=rx.breakpoints(initial="2", sm="3"),
                color="#E2E8F0",
                text_align="center",
                max_width="760px",
                style=STYLE_TEXT_RESPONSIVE,
            ),
            # Grade de 2 colunas: Informações de Acesso + Mapa Interativo
            rx.grid(
                # Card 1: Campus Brejo Santo - UFCA
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.box(
                                rx.icon(tag="map-pin", size=24, color=COLOR_CYAN),
                                background="rgba(0, 173, 181, 0.15)",
                                border_radius="10px",
                                padding="0.6rem",
                                display="grid",
                                place_items="center",
                            ),
                            rx.vstack(
                                rx.heading("Campus Brejo Santo – UFCA", size="4", weight="bold", color=COLOR_TEXT_PRIMARY, style=STYLE_HEADING_RESPONSIVE),
                                rx.text("Instituto de Formação de Educadores (IFE)", size="2", color=COLOR_CYAN_LIGHT, style=STYLE_HEADING_RESPONSIVE),
                                rx.text("Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE • CEP 63260-000", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="center",
                            width="100%",
                        ),
                        rx.divider(color_scheme="gray", opacity="0.15"),
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="plane", size=16, color=COLOR_CYAN),
                                rx.text("Aeroporto de Juazeiro do Norte (JDO) a ~65 km", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                                spacing="1",
                            ),
                            rx.hstack(
                                rx.icon(tag="bus", size=16, color=COLOR_CYAN),
                                rx.text("Conexão direta pelas rodovias federais BR-116 e CE-397", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                                spacing="1",
                            ),
                            spacing="3",
                            wrap="wrap",
                        ),
                        spacing="3",
                        align="start",
                        width="100%",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    width="100%",
                    background=COLOR_SURFACE_GLASS,
                    backdrop_filter="blur(16px)",
                    border=f"1px solid {COLOR_BORDER_CYAN}",
                    box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                ),
                # Card 2: Mapa Interativo Clicável que abre o Google Maps
                rx.link(
                    rx.card(
                        rx.vstack(
                            rx.hstack(
                                rx.box(
                                    rx.icon(tag="navigation", size=24, color="#34d399"),
                                    background="rgba(52, 211, 153, 0.15)",
                                    border_radius="10px",
                                    padding="0.6rem",
                                    display="grid",
                                    place_items="center",
                                ),
                                rx.vstack(
                                    rx.heading("Navegar via Google Maps", size="4", weight="bold", color=COLOR_TEXT_PRIMARY, style=STYLE_HEADING_RESPONSIVE),
                                    rx.text("Coordenadas geográficas exatas do Campus UFCA", size="1", color="#CBD5E1", style=STYLE_TEXT_RESPONSIVE),
                                    spacing="0",
                                    align="start",
                                ),
                                rx.spacer(),
                                rx.badge("Abrir Rota", color_scheme="green", size="2", style=STYLE_BUTTON_CHIP),
                                spacing="3",
                                align="center",
                                width="100%",
                            ),
                            # Visual representativo de mapa
                            rx.box(
                                rx.vstack(
                                    rx.icon(tag="map", size=36, color=COLOR_CYAN),
                                    rx.text("Clique para abrir o trajeto no Google Maps", size="2", weight="medium", color=COLOR_TEXT_PRIMARY),
                                    rx.text("Brejo Santo, Ceará • Região Metropolitana do Cariri", size="1", color="#CBD5E1"),
                                    spacing="1",
                                    align="center",
                                    justify="center",
                                ),
                                height="110px",
                                width="100%",
                                border_radius="12px",
                                background="linear-gradient(135deg, rgba(16, 52, 96, 0.6) 0%, rgba(6, 8, 20, 0.8) 100%)",
                                border=f"1px dashed {COLOR_BORDER_CYAN}",
                                display="grid",
                                place_items="center",
                                margin_top="0.5rem",
                            ),
                            spacing="2",
                            align="start",
                            width="100%",
                        ),
                        padding="1.5rem",
                        border_radius="16px",
                        width="100%",
                        background=COLOR_SURFACE_GLASS,
                        backdrop_filter="blur(16px)",
                        border=f"1px solid {COLOR_BORDER_CYAN}",
                        box_shadow="0 8px 30px rgba(0, 0, 0, 0.35)",
                        _hover={
                            "border_color": "#34d399",
                            "transform": "translateY(-2px)",
                            "box_shadow": "0 10px 32px rgba(52, 211, 153, 0.25)",
                        },
                        transition="all 0.2s ease",
                    ),
                    href=maps_url,
                    is_external=True,
                    width="100%",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                max_width="1060px",
                width="100%",
            ),
            # Grade de Instituições com Logotipos Oficiais e Links Oficiais (CNPq DGP removido)
            rx.vstack(
                rx.text("Instituições Executoras, Parcerias Acadêmicas e Fomento Oficial:", size="2", weight="bold", color=COLOR_TEXT_PRIMARY),
                rx.flex(
                    _instituicao_link_chip("UFCA / IFE", "Instituição Executora", "https://www.ufca.edu.br", "ufca.png"),
                    _instituicao_link_chip("FUNCAP", "Fomento Oficial • Ceará", "https://www.ce.gov.br/funcap/", "funcap.png"),
                    _instituicao_link_chip("Governo do Ceará", "Apoio Institucional", "https://www.ce.gov.br/", "governo_ceara.png"),
                    _instituicao_link_chip("ITA", "Docência e Pesquisa", "http://www.ita.br", "ita.png"),
                    _instituicao_link_chip("CBPF", "Física de Partículas", "https://www.gov.br/cbpf/pt-br", "cbpf.png"),
                    _instituicao_link_chip("UFRGS", "Inovação e Ensino", "https://www.ufrgs.br", "ufrgs.png"),
                    _instituicao_link_chip("UFPB", "Astrofísica Teórica", "https://www.ufpb.br", "ufpb.png"),
                    _instituicao_link_chip("IFCE", "Ciência e Tecnologia", "https://ifce.edu.br", "ifce.png"),
                    _instituicao_link_chip("UECE", "Gravitação e Cosmologia", "https://www.uece.br", "uece.png"),
                    _instituicao_link_chip("URCA", "Polo Regional Cariri", "https://www.urca.br", "urca.png"),
                    _instituicao_link_chip("Planetarium Kariri", "Divulgação Científica", "https://planetariumkariri.ufca.edu.br/", "planetarium.png"),
                    gap="2",
                    wrap="wrap",
                    justify="center",
                    max_width="1060px",
                ),
                spacing="2",
                align="center",
                width="100%",
                margin_top="1.2rem",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="2rem",
        ),
        width="100%",
        id="local",
    )
