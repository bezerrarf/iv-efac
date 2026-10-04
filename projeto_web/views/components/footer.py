"""Rodapé acadêmico oficial do IV EFAC (View).
Régua de marcas de fomento e instituições parceiras, comitê técnico e contatos.
"""

import reflex as rx


def parceiro_chip(nome: str, papel: str, cor: str = "indigo") -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(nome, size="2", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.text(papel, size="1", color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)")),
            spacing="0",
            align="center",
        ),
        padding="0.6rem 1.2rem",
        border_radius="10px",
        background=rx.color_mode_cond(light="rgba(255, 255, 255, 0.9)", dark="rgba(15, 23, 42, 0.6)"),
        border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.08)"),
        box_shadow="0 2px 8px rgba(0, 0, 0, 0.04)",
    )


def footer() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.divider(color_scheme="gray", opacity="0.2"),
            # Régua de Logos e Parceiros Institucionais
            rx.vstack(
                rx.text(
                    "Fomento Oficial & Instituições Parceiras",
                    size="1",
                    weight="bold",
                    text_transform="uppercase",
                    letter_spacing="0.1em",
                    color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"),
                ),
                rx.flex(
                    parceiro_chip("FUNCAP", "Edital 03/2026 • Fomento Oficial"),
                    parceiro_chip("Governo do Ceará", "Fomento à C&T"),
                    parceiro_chip("UFCA / IFE", "Instituição Executora • Brejo Santo"),
                    parceiro_chip("ITA", "Instituto Tecnológico de Aeronáutica"),
                    parceiro_chip("CBPF", "Centro Brasileiro de Pesquisas Físicas"),
                    parceiro_chip("UFRGS", "Univ. Federal do Rio Grande do Sul"),
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
            rx.divider(color_scheme="gray", opacity="0.15"),
            # Informações detalhadas e contatos
            rx.hstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon(
                            tag="telescope",
                            size=22,
                            color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                        ),
                        rx.heading(
                            "IV EFAC 2026",
                            size="4",
                            weight="bold",
                            color=rx.color_mode_cond(light="#103460", dark="white"),
                        ),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "Encontro de Física e Astronomia do Cariri",
                        size="2",
                        weight="medium",
                        color=rx.color_mode_cond(light="#334155", dark="var(--gray-11)"),
                    ),
                    rx.text(
                        "11 e 12 de Novembro de 2026 • Campus Brejo Santo – UFCA",
                        size="2",
                        color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)"),
                    ),
                    rx.text(
                        "Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE",
                        size="1",
                        color=rx.color_mode_cond(light="#94a3b8", dark="var(--gray-8)"),
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
                        color=rx.color_mode_cond(light="#103460", dark="white"),
                    ),
                    rx.text(
                        "Coord. Geral: Prof. Dr. Edson Otoniel da Silva & Prof. Dr. André Flávio Gonçalves Silva",
                        size="2",
                        color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    ),
                    rx.link(
                        "edson.otoniel@ufca.edu.br",
                        href="mailto:edson.otoniel@ufca.edu.br",
                        size="2",
                        color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"),
                    ),
                    rx.text(
                        "Processo FUNCAP: CER-0264-00190.01.00/26",
                        size="1",
                        color=rx.color_mode_cond(light="#94a3b8", dark="var(--gray-8)"),
                    ),
                    align="end",
                    spacing="1",
                ),
                width="100%",
                max_width="1280px",
                margin="0 auto",
                padding="2rem 1.5rem",
                justify="between",
                wrap="wrap",
            ),
            rx.text(
                "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Desenvolvido com Reflex & SQLite WAL.",
                size="1",
                color=rx.color_mode_cond(light="#94a3b8", dark="var(--gray-8)"),
                text_align="center",
                padding_bottom="1.5rem",
            ),
            width="100%",
            spacing="1",
        ),
        background=rx.color_mode_cond(light="#f8fafc", dark="rgba(6, 8, 20, 0.97)"),
        border_top=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.06)"),
        width="100%",
        margin_top="auto",
    )
