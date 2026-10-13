"""Rodapé acadêmico oficial do IV EFAC (View Cósmica).
Comitê técnico, contatos e copyright oficial com visibilidade garantida.
"""

import reflex as rx


def parceiro_chip(nome: str = "", logo: str = "") -> rx.Component:
    """Compatibilidade retroativa."""
    return rx.fragment()


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.divider(color_scheme="gray", opacity="0.25"),
            # Informações detalhadas e contatos
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            tag="telescope",
                            size=24,
                            color="#00ADB5",
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
                        color="#E2E8F0",
                    ),
                    rx.text(
                        "11 e 12 de Novembro de 2026 • Campus Brejo Santo – UFCA",
                        size="2",
                        color="#CBD5E1",
                    ),
                    rx.text(
                        "Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE",
                        size="1",
                        color="#94A3B8",
                    ),
                    align="start",
                    spacing="1",
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
                        color="#E2E8F0",
                    ),
                    rx.link(
                        "edson.otoniel@ufca.edu.br",
                        href="mailto:edson.otoniel@ufca.edu.br",
                        size="2",
                        color="#38bdf8",
                    ),
                    rx.text(
                        "Processo FUNCAP: CER-0264-00190.01.00/26",
                        size="1",
                        color="#94A3B8",
                    ),
                    align=rx.breakpoints(initial="start", sm="end"),
                    spacing="1",
                ),
                width="100%",
                max_width="1280px",
                margin="0 auto",
                padding="2rem 1.5rem 1.5rem 1.5rem",
                justify="between",
                wrap="wrap",
            ),
            # Barra Inferior de Créditos com Destaque Visual Garantido
            rx.box(
                rx.text(
                    "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Desenvolvido por Ramon Firmino Bezerra.",
                    size="2",
                    weight="medium",
                    color="#FFFFFF",
                    text_align="center",
                    style={
                        "color": "#FFFFFF !important",
                        "textAlign": "center",
                        "letterSpacing": "0.02em",
                    },
                ),
                width="100%",
                padding_y="1.2rem",
                padding_x="1rem",
                background="rgba(3, 5, 12, 0.98)",
                border_top="1px solid rgba(255, 255, 255, 0.12)",
                display="flex",
                justify_content="center",
                align_items="center",
                margin_top="1rem",
            ),
            width="100%",
            spacing="1",
        ),
        position="relative",
        z_index="10",
        background="rgba(6, 8, 20, 0.98)",
        border_top="1px solid rgba(0, 173, 181, 0.25)",
        box_shadow="0 -10px 40px rgba(0, 0, 0, 0.8)",
        width="100%",
        margin_top="auto",
    )
