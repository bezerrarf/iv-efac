"""Rodapé acadêmico oficial do IV EFAC (View - UI/UX Pro Max).
Régua de marcas de fomento e instituições parceiras, comitê técnico e contatos.
Pure Deep Cosmic Dark Theme com responsividade completa para todas as telas.
"""

import reflex as rx
from projeto_web.styles.theme import (
    COLOR_FOOTER_BG,
    COLOR_BORDER_SUBTLE,
    COLOR_BORDER_CYAN,
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_SURFACE_GLASS,
    STYLE_TEXT_RESPONSIVE,
    STYLE_BUTTON_CHIP,
)


def parceiro_chip(nome: str, papel: str) -> rx.Component:
    """Chip de instituição parceira ou agência de fomento com micro-interação."""
    return rx.box(
        rx.vstack(
            rx.text(nome, size="2", weight="bold", color="white"),
            rx.text(papel, size="1", color="var(--gray-9)"),
            spacing="0",
            align="center",
        ),
        padding="0.6rem 1.1rem",
        border_radius="10px",
        background=COLOR_SURFACE_GLASS,
        border=f"1px solid {COLOR_BORDER_SUBTLE}",
        box_shadow="0 4px 16px rgba(0, 0, 0, 0.25)",
        _hover={
            "border_color": COLOR_CYAN,
            "transform": "translateY(-2px)",
            "box_shadow": "0 6px 20px rgba(0, 173, 181, 0.2)",
        },
        transition="all 0.2s ease",
        style=STYLE_BUTTON_CHIP,
    )


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.divider(color_scheme="gray", opacity="0.15"),
            # Régua de Logos e Parceiros Institucionais
            rx.vstack(
                rx.text(
                    "Fomento Oficial & Instituições Parceiras",
                    size="1",
                    weight="bold",
                    text_transform="uppercase",
                    letter_spacing="0.12em",
                    color=COLOR_CYAN_LIGHT,
                ),
                rx.flex(
                    parceiro_chip("FUNCAP", "Edital 03/2026 • Fomento Oficial"),
                    parceiro_chip("Governo do Ceará", "Fomento à C&T"),
                    parceiro_chip("UFCA / IFE", "Instituição Executora • Brejo Santo"),
                    parceiro_chip("ITA", "Inst. Tecnológico de Aeronáutica"),
                    parceiro_chip("CBPF", "Centro Bras. de Pesquisas Físicas"),
                    parceiro_chip("UFRGS", "Univ. Fed. do Rio Grande do Sul"),
                    parceiro_chip("UFPB", "Univ. Federal da Paraíba"),
                    parceiro_chip("IFCE", "Instituto Federal do Ceará"),
                    parceiro_chip("UECE", "Univ. Estadual do Ceará"),
                    parceiro_chip("URCA", "Univ. Regional do Cariri"),
                    parceiro_chip("Observatório Kariri", "Divulgação Científica"),
                    gap="2",
                    wrap="wrap",
                    justify="center",
                    width="100%",
                ),
                spacing="3",
                align="center",
                width="100%",
                padding_y="2rem",
            ),
            rx.divider(color_scheme="gray", opacity="0.12"),
            # Informações detalhadas e contatos adaptados para Mobile & Desktop
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            tag="telescope",
                            size=22,
                            color=COLOR_CYAN,
                        ),
                        rx.heading(
                            "IV EFAC 2026",
                            size="4",
                            weight="bold",
                            color="white",
                        ),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "Encontro de Física e Astronomia do Cariri",
                        size="2",
                        weight="medium",
                        color="var(--gray-11)",
                    ),
                    rx.text(
                        "11 e 12 de Novembro de 2026 • Campus Brejo Santo – UFCA",
                        size="2",
                        color="var(--gray-9)",
                    ),
                    rx.text(
                        "Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE",
                        size="1",
                        color="var(--gray-8)",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    align="start",
                    spacing="1",
                    max_width=["100%", "450px"],
                ),
                rx.spacer(),
                rx.vstack(
                    rx.text(
                        "Coordenação & Comitê",
                        weight="bold",
                        size="2",
                        color="white",
                    ),
                    rx.text(
                        "Coord. Geral: Prof. Dr. Edson Otoniel da Silva & Prof. Dr. André Flávio Gonçalves Silva",
                        size="2",
                        color="var(--gray-10)",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    rx.link(
                        "edson.otoniel@ufca.edu.br",
                        href="mailto:edson.otoniel@ufca.edu.br",
                        size="2",
                        color=COLOR_CYAN_LIGHT,
                        style=STYLE_TEXT_RESPONSIVE,
                        _hover={"text_decoration": "underline"},
                    ),
                    rx.text(
                        "Processo FUNCAP: CER-0264-00190.01.00/26",
                        size="1",
                        color="var(--gray-8)",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    align="start",
                    spacing="1",
                    max_width=["100%", "480px"],
                    margin_top=["1.5rem", "0"],
                ),
                width="100%",
                max_width="1280px",
                margin="0 auto",
                padding="2rem 1.5rem",
                justify="between",
                wrap="wrap",
                align="start",
            ),
            rx.text(
                "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Desenvolvido com Reflex & SQLite WAL.",
                size="1",
                color="var(--gray-8)",
                text_align="center",
                padding_bottom="1.5rem",
            ),
            width="100%",
            spacing="1",
        ),
        background=COLOR_FOOTER_BG,
        border_top=f"1px solid {COLOR_BORDER_SUBTLE}",
        width="100%",
        margin_top="auto",
        position="relative",
        z_index="2",
    )
