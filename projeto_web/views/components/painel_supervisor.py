"""Painel de Supervisão e Conferência de Presença do IV EFAC (View - UI/UX Pro Max).
Acessível a participantes com privilégios de Supervisor e ao Administrador.
Permite:
1. Buscar participantes por Código de Check-in ou Nome.
2. Confirmar presenças em tempo real durante as atividades do evento (11 e 12/11/2026).
3. Visualizar estatísticas de quórum e imprimir a lista de conferência.
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_BORDER_CYAN,
    COLOR_BORDER_SUBTLE,
    COLOR_SURFACE_GLASS,
    STYLE_BUTTON_CHIP,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)


def painel_supervisor_view() -> rx.Component:
    """Componente oficial de credenciamento e conferência de presença durante as atividades."""
    return rx.box(
        rx.vstack(
            # Topo com Badges e Informações da Atividade
            rx.hstack(
                rx.badge("Supervisão de Credenciamento", color_scheme="violet", variant="solid", size="2"),
                rx.badge("Conferência de Presença em Tempo Real", color_scheme="cyan", variant="soft", size="2"),
                rx.spacer(),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="file-spreadsheet", size=14),
                            rx.text("Baixar CSV", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        variant="surface",
                        color_scheme="green",
                        on_click=EventoState.exportar_inscritos_csv,
                        style=STYLE_BUTTON_CHIP,
                        id="btn-superv-export-csv",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="file-down", size=14),
                            rx.text("Baixar PDF Oficial", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        variant="solid",
                        color_scheme="cyan",
                        on_click=EventoState.exportar_inscritos_pdf,
                        style=STYLE_BUTTON_CHIP,
                        id="btn-superv-export-pdf",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="printer", size=14),
                            rx.text("Imprimir Lista", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        variant="outline",
                        color_scheme="gray",
                        on_click=rx.call_script("window.print()"),
                        style=STYLE_BUTTON_CHIP,
                    ),
                    spacing="2",
                    align="center",
                ),
                width="100%",
                align="center",
                wrap="wrap",
                gap="2",
            ),
            rx.heading("Lista de Conferência de Inscritos • Atividades do IV EFAC", size="6", weight="bold", color="white"),
            rx.text(
                "Utilize o leitor de código ou busque pelo nome/e-mail para registrar a entrada dos congressistas nas palestras e minicursos no Campus Brejo Santo.",
                size="2",
                color="var(--gray-10)",
            ),
            # Placar de Presença
            rx.hstack(
                rx.box(
                    rx.hstack(
                        rx.icon(tag="user-check", size=24, color="#34d399"),
                        rx.vstack(
                            rx.heading(f"{EventoState.superv_presentes_count} / {EventoState.superv_total_count}", size="6", weight="bold", color="white"),
                            rx.text("Presentes Confirmados", size="1", color="var(--gray-9)"),
                            spacing="0",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    background="rgba(15, 23, 42, 0.8)",
                    border="1px solid rgba(52, 211, 153, 0.3)",
                    border_radius="12px",
                    padding="0.85rem 1.25rem",
                ),
                rx.box(
                    rx.hstack(
                        rx.icon(tag="clock", size=24, color="#38bdf8"),
                        rx.vstack(
                            rx.heading("11 e 12 Nov 2026", size="5", weight="bold", color="white"),
                            rx.text("Campus Brejo Santo – UFCA", size="1", color="var(--gray-9)"),
                            spacing="0",
                        ),
                        spacing="3",
                        align="center",
                    ),
                    background="rgba(15, 23, 42, 0.8)",
                    border="1px solid rgba(56, 189, 248, 0.3)",
                    border_radius="12px",
                    padding="0.85rem 1.25rem",
                ),
                spacing="3",
                wrap="wrap",
            ),
            # Campo de Busca Rápida de Check-in
            rx.hstack(
                rx.input(
                    placeholder="Digitar ou bipar código (ex: ASTRO-...) ou nome do participante...",
                    value=EventoState.superv_busca,
                    on_change=EventoState.set_superv_busca,
                    size="3",
                    flex="1",
                ),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="search", size=16),
                        rx.text("Buscar", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    size="3",
                    color_scheme="violet",
                    on_click=EventoState.carregar_painel_supervisor,
                    style=STYLE_BUTTON_CHIP,
                ),
                width="100%",
                spacing="2",
            ),
            # Tabela de Conferência
            rx.box(
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Código Check-in"),
                            rx.table.column_header_cell("Nome do Participante"),
                            rx.table.column_header_cell("Polo / Modalidade"),
                            rx.table.column_header_cell("Status"),
                            rx.table.column_header_cell("Ação de Presença"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(
                            EventoState.superv_inscritos,
                            lambda item: rx.table.row(
                                rx.table.cell(
                                    rx.badge(item["codigo"], color_scheme="cyan", variant="solid", size="2"),
                                ),
                                rx.table.cell(
                                    rx.vstack(
                                        rx.text(item["nome"], size="2", weight="bold", color="white"),
                                        rx.text(item["email"], size="1", color="var(--gray-9)"),
                                        spacing="0",
                                    ),
                                ),
                                rx.table.cell(
                                    rx.vstack(
                                        rx.badge(item["modalidade"], color_scheme="indigo", variant="surface", size="1"),
                                        rx.text(item["instituicao"], size="1", color="var(--gray-10)"),
                                        spacing="0",
                                    ),
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        item["presenca_confirmada"],
                                        rx.badge("PRESENTE", color_scheme="green", variant="solid", size="2"),
                                        rx.badge("AGUARDANDO", color_scheme="amber", variant="soft", size="1"),
                                    ),
                                ),
                                rx.table.cell(
                                    rx.cond(
                                        item["presenca_confirmada"],
                                        rx.button(
                                            "Desmarcar",
                                            size="1",
                                            variant="ghost",
                                            color_scheme="red",
                                            on_click=EventoState.alternar_presenca_participante(item["id"]),
                                            style=STYLE_BUTTON_CHIP,
                                        ),
                                        rx.button(
                                            "Confirmar Presença",
                                            size="2",
                                            variant="solid",
                                            color_scheme="green",
                                            on_click=EventoState.alternar_presenca_participante(item["id"]),
                                            style=STYLE_BUTTON_CHIP,
                                        ),
                                    ),
                                ),
                                align="center",
                            ),
                        ),
                    ),
                    width="100%",
                    variant="surface",
                ),
                width="100%",
                overflow_x="auto",
                border_radius="12px",
                border="1px solid rgba(255, 255, 255, 0.08)",
            ),
            spacing="4",
            width="100%",
        ),
        background="linear-gradient(145deg, rgba(14, 18, 38, 0.95), rgba(28, 22, 54, 0.9))",
        border="1.5px solid rgba(139, 92, 246, 0.35)",
        box_shadow="0 14px 45px rgba(0, 0, 0, 0.5)",
        border_radius="18px",
        padding=rx.breakpoints(initial="1.25rem", sm="2rem"),
        width="100%",
        margin_top="1.5rem",
    )
