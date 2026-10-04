"""Painel Administrativo Oficial do IV EFAC (View - UI/UX Pro Max).
Exclusivo para o Super Administrador Geral do Evento.
Permite:
1. Analisar participantes inscritos e estatísticas globais.
2. Alterar datas, horários, temas e palestrantes diretamente pelo site.
3. Conceder e revogar poderes de Supervisor para qualquer participante.
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


def stat_metric_box(valor: any, rotulo: str, icone: str, cor: str) -> rx.Component:
    """Card de métrica analítica com micro-brilho."""
    return rx.box(
        rx.hstack(
            rx.box(
                rx.icon(tag=icone, size=22, color=cor),
                background="rgba(255, 255, 255, 0.05)",
                border_radius="10px",
                padding="0.6rem",
                display="grid",
                place_items="center",
            ),
            rx.vstack(
                rx.heading(valor, size="6", weight="bold", color="white"),
                rx.text(rotulo, size="1", color="var(--gray-9)"),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        background="rgba(15, 23, 42, 0.8)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        border_radius="12px",
        padding="1rem",
        flex="1",
        min_width=["140px", "180px"],
    )


def tabela_inscritos_admin() -> rx.Component:
    """Tabela analítica de participantes com concessão de poderes de supervisor."""
    return rx.vstack(
        # Barra de Pesquisa e Filtros
        rx.hstack(
            rx.input(
                placeholder="Buscar por nome, e-mail, código de inscrição ou polo...",
                value=EventoState.admin_filtro_busca,
                on_change=EventoState.set_admin_filtro,
                size="2",
                flex="1",
            ),
            rx.button(
                rx.hstack(
                    rx.icon(tag="refresh-cw", size=14),
                    rx.text("Recarregar", size="1"),
                    spacing="1",
                    align="center",
                ),
                size="2",
                variant="surface",
                color_scheme="gray",
                on_click=EventoState.carregar_painel_admin,
                style=STYLE_BUTTON_CHIP,
            ),
            width="100%",
            spacing="2",
        ),
        # Lista de Inscritos
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Código"),
                        rx.table.column_header_cell("Participante"),
                        rx.table.column_header_cell("Modalidade / Polo"),
                        rx.table.column_header_cell("Função / Role"),
                        rx.table.column_header_cell("Presença"),
                        rx.table.column_header_cell("Ações de Admin"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        EventoState.admin_inscritos,
                        lambda u: rx.table.row(
                            rx.table.cell(
                                rx.badge(u["codigo"], color_scheme="cyan", variant="soft", size="1"),
                            ),
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(u["nome"], size="2", weight="bold", color="white"),
                                    rx.text(u["email"], size="1", color="var(--gray-9)"),
                                    spacing="0",
                                ),
                            ),
                            rx.table.cell(
                                rx.vstack(
                                    rx.badge(u["modalidade"], color_scheme="indigo", variant="surface", size="1"),
                                    rx.text(u["instituicao"], size="1", color="var(--gray-10)"),
                                    spacing="0",
                                ),
                            ),
                            rx.table.cell(
                                rx.cond(
                                    u["role"] == "admin",
                                    rx.badge("Super Admin", color_scheme="red", variant="solid", size="1"),
                                    rx.cond(
                                        u["is_supervisor"],
                                        rx.badge("Supervisor", color_scheme="violet", variant="solid", size="1"),
                                        rx.badge("Participante", color_scheme="gray", variant="surface", size="1"),
                                    ),
                                ),
                            ),
                            rx.table.cell(
                                rx.cond(
                                    u["presenca_confirmada"],
                                    rx.badge("Presente", color_scheme="green", variant="solid", size="1"),
                                    rx.badge("Pendente", color_scheme="amber", variant="surface", size="1"),
                                ),
                            ),
                            rx.table.cell(
                                rx.cond(
                                    u["role"] != "admin",
                                    rx.cond(
                                        u["is_supervisor"],
                                        rx.button(
                                            "Revogar Supervisor",
                                            size="1",
                                            variant="outline",
                                            color_scheme="red",
                                            on_click=EventoState.rebaixar_supervisor(u["id"]),
                                            style=STYLE_BUTTON_CHIP,
                                        ),
                                        rx.button(
                                            "Tornar Supervisor",
                                            size="1",
                                            variant="solid",
                                            color_scheme="violet",
                                            on_click=EventoState.promover_supervisor(u["id"]),
                                            style=STYLE_BUTTON_CHIP,
                                        ),
                                    ),
                                    rx.text("Admin Supremo", size="1", color="var(--gray-9)"),
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
        spacing="3",
        width="100%",
    )


def editor_atividades_admin() -> rx.Component:
    """Editor completo de palestras, temas e horários da grade oficial."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Gestão da Grade de Palestras & Horários", size="4", weight="bold", color="white"),
                rx.text(
                    "Altere datas, horários e temas diretamente pelo site. As alterações refletem imediatamente no cronograma público.",
                    size="2",
                    color="var(--gray-10)",
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.button(
                rx.hstack(
                    rx.icon(tag="rotate-ccw", size=14),
                    rx.text("Restaurar Grade Padrão", size="1"),
                    spacing="1",
                    align="center",
                ),
                size="2",
                variant="outline",
                color_scheme="amber",
                on_click=EventoState.restaurar_grade_padrao,
                style=STYLE_BUTTON_CHIP,
            ),
            width="100%",
            align="center",
            wrap="wrap",
            gap="2",
        ),
        # Formulário Modal/Inline de Edição (Aparece quando is_editing_atividade é True)
        rx.cond(
            EventoState.is_editing_atividade,
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="edit-3", size=18, color=COLOR_CYAN),
                        rx.heading("Editar Atividade / Palestra", size="3", weight="bold", color="white"),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=16),
                            variant="ghost",
                            size="1",
                            on_click=EventoState.fechar_edicao_atividade,
                        ),
                        width="100%",
                        align="center",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Dia do Evento", size="1", weight="bold", color="var(--gray-9)"),
                            rx.select(
                                ["Dia 1", "Dia 2"],
                                value=EventoState.edit_ativ_dia,
                                on_change=EventoState.set_edit_ativ_dia,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Faixa Horária", size="1", weight="bold", color="var(--gray-9)"),
                            rx.input(
                                value=EventoState.edit_ativ_horario,
                                on_change=EventoState.set_edit_ativ_horario,
                                placeholder="Ex: 09:30 – 10:30",
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Tipo / Sessão", size="1", weight="bold", color="var(--gray-9)"),
                            rx.input(
                                value=EventoState.edit_ativ_tipo,
                                on_change=EventoState.set_edit_ativ_tipo,
                                placeholder="Ex: Palestra Convidada",
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        columns=rx.breakpoints(initial="1", sm="3"),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Título / Tema da Palestra", size="1", weight="bold", color="var(--gray-9)"),
                        rx.input(
                            value=EventoState.edit_ativ_titulo,
                            on_change=EventoState.set_edit_ativ_titulo,
                            placeholder="Tema oficial da apresentação",
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Palestrante / Convidado", size="1", weight="bold", color="var(--gray-9)"),
                            rx.input(
                                value=EventoState.edit_ativ_palestrante,
                                on_change=EventoState.set_edit_ativ_palestrante,
                                placeholder="Nome do(a) pesquisador(a)",
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Local", size="1", weight="bold", color="var(--gray-9)"),
                            rx.input(
                                value=EventoState.edit_ativ_local,
                                on_change=EventoState.set_edit_ativ_local,
                                placeholder="Auditório Central, Sala Temática...",
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2"),
                        spacing="2",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Descrição / Resumo da Atividade", size="1", weight="bold", color="var(--gray-9)"),
                        rx.text_area(
                            value=EventoState.edit_ativ_descricao,
                            on_change=EventoState.set_edit_ativ_descricao,
                            placeholder="Detalhes sobre os tópicos abordados...",
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            variant="ghost",
                            size="2",
                            on_click=EventoState.fechar_edicao_atividade,
                        ),
                        rx.button(
                            "Salvar Alterações na Grade",
                            variant="solid",
                            color_scheme="cyan",
                            size="2",
                            on_click=EventoState.salvar_edicao_atividade,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        spacing="2",
                        justify="end",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                background="rgba(10, 16, 35, 0.95)",
                border="1.5px solid rgba(0, 173, 181, 0.5)",
                border_radius="14px",
                padding="1.25rem",
                width="100%",
                box_shadow="0 8px 30px rgba(0, 0, 0, 0.5)",
                margin_y="0.5rem",
            ),
        ),
        # Lista / Cards das Atividades Salvas
        rx.box(
            rx.vstack(
                rx.foreach(
                    EventoState.admin_atividades,
                    lambda at: rx.card(
                        rx.hstack(
                            rx.badge(at["dia"], color_scheme="indigo", variant="surface", size="1"),
                            rx.badge(at["horario"], color_scheme="cyan", variant="solid", size="1"),
                            rx.vstack(
                                rx.text(at["titulo"], size="2", weight="bold", color="white"),
                                rx.hstack(
                                    rx.text(at["palestrante"], size="1", color=COLOR_CYAN_LIGHT),
                                    rx.text("•", size="1", color="var(--gray-8)"),
                                    rx.text(at["local"], size="1", color="var(--gray-9)"),
                                    spacing="1",
                                    align="center",
                                ),
                                spacing="0",
                                align="start",
                                flex="1",
                            ),
                            rx.button(
                                rx.hstack(
                                    rx.icon(tag="pencil", size=13),
                                    rx.text("Editar", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                size="1",
                                variant="surface",
                                color_scheme="cyan",
                                on_click=EventoState.abrir_edicao_atividade(at["id"]),
                                style=STYLE_BUTTON_CHIP,
                            ),
                            align="center",
                            width="100%",
                            spacing="3",
                        ),
                        background="rgba(15, 23, 42, 0.7)",
                        border="1px solid rgba(255, 255, 255, 0.06)",
                        padding="0.75rem",
                        width="100%",
                    ),
                ),
                spacing="2",
                width="100%",
            ),
            width="100%",
            max_height="450px",
            overflow_y="auto",
        ),
        spacing="3",
        width="100%",
    )


def painel_admin_view() -> rx.Component:
    """Componente completo de renderização do Painel de Administração."""
    return rx.box(
        rx.vstack(
            # Título e Badges
            rx.hstack(
                rx.badge("Acesso Exclusivo Super Admin", color_scheme="red", variant="solid", size="2"),
                rx.badge("Controle Total do Evento", color_scheme="cyan", variant="soft", size="2"),
                spacing="2",
                align="center",
            ),
            rx.heading("Painel de Controle Administrativo • IV EFAC", size="6", weight="bold", color="white"),
            # Grid de Métricas
            rx.grid(
                stat_metric_box(EventoState.admin_total_inscritos, "Total de Inscritos", "users", "#38bdf8"),
                stat_metric_box(EventoState.admin_total_presenciais, "Vagas Presenciais", "building", "#818cf8"),
                stat_metric_box(EventoState.admin_total_onlines, "Transmissão Online", "globe", "#34d399"),
                stat_metric_box(EventoState.admin_total_presentes, "Presenças Confirmadas", "check-circle", "#f59e0b"),
                stat_metric_box(EventoState.admin_total_supervisores, "Supervisores Ativos", "shield", "#c084fc"),
                columns=rx.breakpoints(initial="2", sm="3", md="5"),
                spacing="3",
                width="100%",
            ),
            # Abas do Admin: Inscritos vs Editor de Grade
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="users", size=14),
                            rx.text("Inscritos & Supervisores", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="inscritos",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="calendar", size=14),
                            rx.text("Editor de Palestras & Grade", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="grade",
                    ),
                    size="2",
                ),
                rx.tabs.content(
                    tabela_inscritos_admin(),
                    value="inscritos",
                    padding_top="1.5rem",
                ),
                rx.tabs.content(
                    editor_atividades_admin(),
                    value="grade",
                    padding_top="1.5rem",
                ),
                default_value="inscritos",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        background="linear-gradient(145deg, rgba(12, 18, 38, 0.95), rgba(20, 32, 60, 0.9))",
        border="1.5px solid rgba(239, 68, 68, 0.35)",
        box_shadow="0 14px 45px rgba(0, 0, 0, 0.5)",
        border_radius="18px",
        padding=rx.breakpoints(initial="1.25rem", sm="2rem"),
        width="100%",
        margin_top="1.5rem",
    )
