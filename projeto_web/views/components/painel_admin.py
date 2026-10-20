"""Painel Administrativo Oficial do IV EFAC (View - UI/UX Pro Max).
Exclusivo para o Administrador Geral do Evento.
Permite:
1. Analisar participantes inscritos e estatísticas globais em tempo real.
2. Criar, alterar e delegar manualmente dias, horários, temas e responsáveis de palestras.
3. Conceder e revogar poderes de Supervisor para qualquer participante.
4. Alterar a senha de qualquer participante e a sua própria senha de Admin.
5. Inspecionar, gerar e emitir a Carteirinha Oficial de qualquer inscrito.
6. Exportar a relação completa de inscritos em formatos CSV e PDF oficial.
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.admin_state import AdminState
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
                rx.text(rotulo, size="1", color="#CBD5E1"),
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


def modal_alterar_senha_inscrito() -> rx.Component:
    """Modal para o administrador redefinir a senha de qualquer participante."""
    return rx.cond(
        AdminState.modal_alterar_senha_aberto,
        rx.box(
            # Backdrop de foco
            rx.box(
                position="fixed",
                inset="0",
                background="rgba(0, 0, 0, 0.8)",
                z_index="1000",
                backdrop_filter="blur(8px)",
                on_click=AdminState.fechar_modal_senha,
            ),
            # Caixa do Modal
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.icon(tag="key", size=22, color=COLOR_CYAN),
                            background="rgba(0, 173, 181, 0.15)",
                            border_radius="8px",
                            padding="0.5rem",
                            display="grid",
                            place_items="center",
                        ),
                        rx.vstack(
                            rx.heading("Alterar Senha do Inscrito", size="4", weight="bold", color="white"),
                            rx.text("Redefinição direta e segura de senha", size="1", color="#CBD5E1"),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            size="1",
                            on_click=AdminState.fechar_modal_senha,
                            cursor="pointer",
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.2"),
                    rx.box(
                        rx.hstack(
                            rx.icon(tag="user", size=16, color="#CBD5E1"),
                            rx.text(
                                "Participante: ",
                                rx.text.strong(AdminState.admin_senha_user_nome, color="white"),
                                size="2",
                                color="#CBD5E1",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        background="rgba(255, 255, 255, 0.04)",
                        padding="0.6rem 0.9rem",
                        border_radius="8px",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Nova Senha", size="2", weight="bold", color="white"),
                        rx.input(
                            placeholder="Digite a nova senha (mínimo 6 caracteres)",
                            type="password",
                            value=AdminState.admin_nova_senha_input,
                            on_change=AdminState.set_admin_nova_senha,
                            size="3",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            variant="outline",
                            color_scheme="gray",
                            size="2",
                            on_click=AdminState.fechar_modal_senha,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="check", size=16),
                                rx.text("Salvar Nova Senha"),
                                spacing="1",
                                align="center",
                            ),
                            variant="solid",
                            color_scheme="cyan",
                            size="2",
                            on_click=AdminState.salvar_nova_senha_inscrito,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                        padding_top="0.5rem",
                    ),
                    spacing="3",
                    width="100%",
                ),
                position="fixed",
                top="50%",
                left="50%",
                transform="translate(-50%, -50%)",
                z_index="1001",
                width="92%",
                max_width="480px",
                background="rgba(15, 23, 42, 0.98)",
                border="1.5px solid rgba(0, 173, 181, 0.4)",
                box_shadow="0 25px 60px rgba(0, 0, 0, 0.8)",
                border_radius="16px",
                padding="1.5rem",
            ),
        ),
        rx.fragment(),
    )


def tabela_inscritos_admin() -> rx.Component:
    """Tabela analítica de participantes com rolagem cinética fluida no mobile e exportação em CSV/PDF."""
    return rx.vstack(
        # Barra Superior: Pesquisa, Recarregar e Botões de Exportação
        rx.hstack(
            rx.input(
                placeholder="Buscar por nome, e-mail, código ou polo...",
                value=AdminState.admin_filtro_busca,
                on_change=AdminState.set_admin_filtro,
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
                on_click=AdminState.carregar_painel_admin,
                style=STYLE_BUTTON_CHIP,
                white_space="nowrap",
            ),
            # Botão Baixar CSV
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
                on_click=AdminState.exportar_inscritos_csv,
                style=STYLE_BUTTON_CHIP,
                id="btn-admin-export-csv",
                white_space="nowrap",
            ),
            # Botão Baixar PDF
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
                on_click=AdminState.exportar_inscritos_pdf,
                style=STYLE_BUTTON_CHIP,
                id="btn-admin-export-pdf",
                white_space="nowrap",
            ),
            width="100%",
            spacing="2",
            wrap="wrap",
        ),
        # Dica Visual de Deslize Horizontal apenas no Mobile
        rx.box(
            rx.hstack(
                rx.icon(tag="arrow-left-right", size=13, color="#00ADB5"),
                rx.text("Deslize para o lado para visualizar todas as presenças e ações", size="1", color="#CBD5E1"),
                spacing="1",
                align="center",
            ),
            display=rx.breakpoints(initial="flex", md="none"),
            padding="0.35rem 0.75rem",
            background="rgba(0, 173, 181, 0.10)",
            border_radius="8px",
            border="1px solid rgba(0, 173, 181, 0.25)",
            width="100%",
        ),
        # Contêiner da Tabela com Scroll Suave e Cinético no Mobile
        # Barra de Rolagem Horizontal no Topo da Tabela (sincronizada via script)
        rx.box(
            rx.box(
                width="100%",
                min_width="850px",
                height="1px",
            ),
            id="admin-table-top-scroll",
            class_name="table-top-scroll-track",
            width="100%",
        ),
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell(
                            "Código",
                            width="120px",
                            min_width="120px",
                            white_space="nowrap",
                        ),
                        rx.table.column_header_cell(
                            "Participante",
                            min_width="240px",
                            white_space="nowrap",
                        ),
                        rx.table.column_header_cell(
                            "Modalidade / Polo",
                            min_width="200px",
                            white_space="nowrap",
                        ),
                        rx.table.column_header_cell(
                            "Presença (D1 | D2)",
                            width="160px",
                            min_width="160px",
                            text_align="center",
                            white_space="nowrap",
                        ),
                        rx.table.column_header_cell(
                            "Ações Administrativas",
                            width="260px",
                            min_width="260px",
                            text_align="center",
                            white_space="nowrap",
                        ),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AdminState.admin_inscritos,
                        lambda u: rx.table.row(
                            # 1. Código Check-in (Monospace, padding elegante, nowrap)
                            rx.table.cell(
                                rx.badge(
                                    u["codigo"],
                                    color_scheme="cyan",
                                    variant="soft",
                                    size="1",
                                    white_space="nowrap",
                                    font_family="monospace",
                                    font_weight="bold",
                                    letter_spacing="0.5px",
                                    padding_x="0.6rem",
                                    padding_y="0.25rem",
                                ),
                                white_space="nowrap",
                            ),
                            # 2. Participante (Nome e e-mail com nowrap e hierarquia clara)
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(u["nome"], size="2", weight="bold", color="white", white_space="nowrap"),
                                    rx.text(u["email"], size="1", color="#CBD5E1", white_space="nowrap"),
                                    spacing="0",
                                    align="start",
                                ),
                                white_space="nowrap",
                            ),
                            # 3. Modalidade e Polo/Instituição
                            rx.table.cell(
                                rx.vstack(
                                    rx.badge(u["modalidade"], color_scheme="indigo", variant="surface", size="1", white_space="nowrap"),
                                    rx.text(u["instituicao"], size="1", color="#CBD5E1", white_space="nowrap"),
                                    spacing="0",
                                    align="start",
                                ),
                                white_space="nowrap",
                            ),
                            # 4. Presença Segregada Dia 1 e Dia 2 (Badges interativos)
                            rx.table.cell(
                                rx.hstack(
                                    rx.tooltip(
                                        rx.badge(
                                            "Dia 1",
                                            color_scheme=rx.cond(u["presenca_dia1"], "green", "gray"),
                                            variant=rx.cond(u["presenca_dia1"], "solid", "surface"),
                                            size="1",
                                            cursor="pointer",
                                            white_space="nowrap",
                                            padding_x="0.55rem",
                                            on_click=AdminState.alternar_presenca_dia(u["id"], "Dia 1"),
                                        ),
                                        content="Presença Dia 1 (11/Nov) • Clique para alternar",
                                    ),
                                    rx.tooltip(
                                        rx.badge(
                                            "Dia 2",
                                            color_scheme=rx.cond(u["presenca_dia2"], "green", "gray"),
                                            variant=rx.cond(u["presenca_dia2"], "solid", "surface"),
                                            size="1",
                                            cursor="pointer",
                                            white_space="nowrap",
                                            padding_x="0.55rem",
                                            on_click=AdminState.alternar_presenca_dia(u["id"], "Dia 2"),
                                        ),
                                        content="Presença Dia 2 (12/Nov) • Clique para alternar",
                                    ),
                                    spacing="1",
                                    align="center",
                                    justify="center",
                                    wrap="nowrap",
                                ),
                                white_space="nowrap",
                                align="center",
                            ),
                            # 5. Ações Administrativas (Editar, Carteirinha, Senha)
                            rx.table.cell(
                                rx.hstack(
                                    # Botão Editar Perfil Completo
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="user-cog", size=12),
                                            rx.text("Editar", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="1",
                                        variant="surface",
                                        color_scheme="cyan",
                                        on_click=AdminState.abrir_modal_editar_participante(u),
                                        style=STYLE_BUTTON_CHIP,
                                        white_space="nowrap",
                                        flex_shrink="0",
                                    ),
                                    
                                    # Botão Alterar Senha do Inscrito
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="key", size=12),
                                            rx.text("Senha", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="1",
                                        variant="surface",
                                        color_scheme="cyan",
                                        on_click=AdminState.abrir_modal_senha(u["id"], u["nome"]),
                                        style=STYLE_BUTTON_CHIP,
                                        white_space="nowrap",
                                        flex_shrink="0",
                                    ),
                                    spacing="2",
                                    align="center",
                                    justify="center",
                                    wrap="nowrap",
                                ),
                                white_space="nowrap",
                                align="center",
                            ),
                            align="center",
                            class_name="interactive-table-row",
                        ),
                    ),
                ),
                width="100%",
                min_width="850px",
                variant="surface",
            ),
            id="admin-table-bottom-scroll",
            class_name="table-scroll-container",
            width="100%",
        ),
        rx.script("""
        (function() {
            function syncTableScroll() {
                var topEl = document.getElementById("admin-table-top-scroll");
                var btmEl = document.getElementById("admin-table-bottom-scroll");
                if (!topEl || !btmEl) return;
                if (topEl._syncAttached) return;
                topEl._syncAttached = true;

                var isSyncingTop = false;
                var isSyncingBtm = false;

                topEl.addEventListener("scroll", function() {
                    if (!isSyncingTop) {
                        isSyncingBtm = true;
                        btmEl.scrollLeft = topEl.scrollLeft;
                    }
                    isSyncingTop = false;
                }, { passive: true });

                btmEl.addEventListener("scroll", function() {
                    if (!isSyncingBtm) {
                        isSyncingTop = true;
                        topEl.scrollLeft = btmEl.scrollLeft;
                    }
                    isSyncingBtm = false;
                }, { passive: true });
            }

            if (document.readyState === "loading") {
                document.addEventListener("DOMContentLoaded", syncTableScroll);
            } else {
                syncTableScroll();
            }
            setInterval(syncTableScroll, 800);
        })();
        """),
        spacing="3",
        width="100%",
    )


def editor_atividades_admin() -> rx.Component:
    """Editor completo de palestras, delegação de responsáveis, temas e horários da grade oficial."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Gestão da Grade de Atividades", size="4", weight="bold", color="white"),
                rx.text(
                    "Gerencie horários, temas, palestrantes e novas atividades da programação oficial.",
                    size="2",
                    color="#CBD5E1",
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                # Botão Criar / Delegar Nova Atividade
                rx.button(
                    rx.hstack(
                        rx.icon(tag="circle-plus", size=14),
                        rx.text("Incluir Nova Atividade", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    size="2",
                    variant="solid",
                    color_scheme="cyan",
                    on_click=AdminState.abrir_criacao_atividade,
                    style=STYLE_BUTTON_CHIP,
                ),
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
                    on_click=AdminState.restaurar_grade_padrao,
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="2",
                align="center",
            ),
            align="center",
            width="100%",
            wrap="wrap",
        ),
        # Formulário para Criar e Delegar Nova Atividade
        rx.cond(
            AdminState.is_creating_atividade,
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="circle-plus", size=18, color=COLOR_CYAN),
                        rx.heading("Incluir Nova Atividade na Grade", size="3", weight="bold", color="white"),
                        rx.spacer(),
                        rx.badge("Nova Atividade", color_scheme="green", size="1"),
                        align="center",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Dia do Evento", size="1", weight="bold", color="white"),
                            rx.select(
                                ["Dia 1", "Dia 2"],
                                value=AdminState.new_ativ_dia,
                                on_change=AdminState.set_new_ativ_dia,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Horário (ex.: 14:00 – 15:30)", size="1", weight="bold", color="white"),
                            rx.input(
                                placeholder="Ex: 14:00 – 15:30",
                                value=AdminState.new_ativ_horario,
                                on_change=AdminState.set_new_ativ_horario,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Tipo de Atividade", size="1", weight="bold", color="white"),
                            rx.select(
                                ["Conferência", "Mesa-Redonda", "Minicurso", "Sessão Oral", "Abertura", "Intervalo"],
                                value=AdminState.new_ativ_tipo,
                                on_change=AdminState.set_new_ativ_tipo,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Local / Sala", size="1", weight="bold", color="white"),
                            rx.input(
                                value=AdminState.new_ativ_local,
                                on_change=AdminState.set_new_ativ_local,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2", md="4"),
                        spacing="3",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Título / Tema da Palestra ou Atividade", size="1", weight="bold", color="white"),
                        rx.input(
                            placeholder="Tema da conferência ou título do minicurso...",
                            value=AdminState.new_ativ_titulo,
                            on_change=AdminState.set_new_ativ_titulo,
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Delegar Responsável / Palestrante", size="1", weight="bold", color="white"),
                        rx.input(
                            placeholder="Nome do palestrante, supervisor ou debatedor responsável...",
                            value=AdminState.new_ativ_palestrante,
                            on_change=AdminState.set_new_ativ_palestrante,
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Ementa / Descrição Detalhada", size="1", weight="bold", color="white"),
                        rx.text_area(
                            placeholder="Breve ementa ou tópicos da atividade...",
                            value=AdminState.new_ativ_descricao,
                            on_change=AdminState.set_new_ativ_descricao,
                            size="2",
                            width="100%",
                            rows="2",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            size="2",
                            variant="ghost",
                            color_scheme="gray",
                            on_click=AdminState.fechar_criacao_atividade,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="check", size=16),
                                rx.text("Criar e Delegar Atividade"),
                                spacing="1",
                                align="center",
                            ),
                            size="2",
                            variant="solid",
                            color_scheme="green",
                            on_click=AdminState.criar_nova_atividade,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        spacing="2",
                        justify="end",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                background="rgba(15, 23, 42, 0.95)",
                border="1.5px solid rgba(34, 197, 94, 0.4)",
                border_radius="14px",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.fragment(),
        ),
        # Formulário de Edição Aberto
        rx.cond(
            AdminState.is_editing_atividade,
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="pencil", size=18, color=COLOR_CYAN),
                        rx.heading("Editar e Re-delegar Atividade", size="3", weight="bold", color="white"),
                        rx.spacer(),
                        rx.badge(f"ID #{AdminState.edit_ativ_id}", color_scheme="cyan", size="1"),
                        align="center",
                        width="100%",
                    ),
                    rx.grid(
                        rx.vstack(
                            rx.text("Dia do Evento (Manual)", size="1", weight="bold", color="white"),
                            rx.select(
                                ["Dia 1", "Dia 2"],
                                value=AdminState.edit_ativ_dia,
                                on_change=AdminState.set_edit_ativ_dia,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Horário (ex.: 14:00 – 15:30)", size="1", weight="bold", color="white"),
                            rx.input(
                                value=AdminState.edit_ativ_horario,
                                on_change=AdminState.set_edit_ativ_horario,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Tipo de Atividade", size="1", weight="bold", color="white"),
                            rx.select(
                                ["Abertura", "Conferência", "Minicurso", "Mesa-Redonda", "Sessão Oral", "Intervalo"],
                                value=AdminState.edit_ativ_tipo,
                                on_change=AdminState.set_edit_ativ_tipo,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Local / Sala", size="1", weight="bold", color="white"),
                            rx.input(
                                value=AdminState.edit_ativ_local,
                                on_change=AdminState.set_edit_ativ_local,
                                size="2",
                                width="100%",
                            ),
                            spacing="1",
                        ),
                        columns=rx.breakpoints(initial="1", sm="2", md="4"),
                        spacing="3",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Tema / Título da Palestra ou Atividade", size="1", weight="bold", color="white"),
                        rx.input(
                            value=AdminState.edit_ativ_titulo,
                            on_change=AdminState.set_edit_ativ_titulo,
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Delegar Palestrante(s) ou Supervisor", size="1", weight="bold", color="white"),
                        rx.input(
                            value=AdminState.edit_ativ_palestrante,
                            on_change=AdminState.set_edit_ativ_palestrante,
                            size="2",
                            width="100%",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.vstack(
                        rx.text("Ementa / Descrição Detalhada", size="1", weight="bold", color="white"),
                        rx.text_area(
                            value=AdminState.edit_ativ_descricao,
                            on_change=AdminState.set_edit_ativ_descricao,
                            size="2",
                            width="100%",
                            rows="2",
                        ),
                        spacing="1",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="trash-2", size=14),
                                rx.text("Excluir Atividade"),
                                spacing="1",
                                align="center",
                            ),
                            size="2",
                            variant="soft",
                            color_scheme="red",
                            on_click=AdminState.excluir_atividade(AdminState.edit_ativ_id),
                            style=STYLE_BUTTON_CHIP,
                        ),
                        rx.spacer(),
                        rx.button(
                            "Cancelar",
                            size="2",
                            variant="ghost",
                            color_scheme="gray",
                            on_click=AdminState.fechar_edicao_atividade,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="check", size=16),
                                rx.text("Salvar Alterações na Grade"),
                                spacing="1",
                                align="center",
                            ),
                            size="2",
                            variant="solid",
                            color_scheme="cyan",
                            on_click=AdminState.salvar_edicao_atividade,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        spacing="2",
                        justify="end",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                background="rgba(15, 23, 42, 0.9)",
                border="1px solid rgba(0, 173, 181, 0.3)",
                border_radius="14px",
                width="100%",
                margin_bottom="1rem",
            ),
            rx.fragment(),
        ),
        # Lista de Atividades Atuais
        rx.box(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Dia", width="90px", min_width="90px", white_space="nowrap"),
                        rx.table.column_header_cell("Horário", width="120px", min_width="120px", white_space="nowrap"),
                        rx.table.column_header_cell("Tipo", width="120px", min_width="120px", white_space="nowrap"),
                        rx.table.column_header_cell("Tema / Atividade", min_width="260px", white_space="nowrap"),
                        rx.table.column_header_cell("Responsável Delegado", min_width="190px", white_space="nowrap"),
                        rx.table.column_header_cell("Ações", width="180px", min_width="180px", text_align="center", white_space="nowrap"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AdminState.admin_atividades,
                        lambda a: rx.table.row(
                            rx.table.cell(rx.badge(a["dia"], color_scheme="indigo", size="1")),
                            rx.table.cell(rx.text(a["horario"], size="2", weight="bold", color="white")),
                            rx.table.cell(rx.badge(a["tipo"], color_scheme="cyan", variant="surface", size="1")),
                            rx.table.cell(
                                rx.vstack(
                                    rx.text(a["titulo"], size="2", weight="bold", color="white"),
                                    rx.text(a["local"], size="1", color="#CBD5E1"),
                                    spacing="0",
                                ),
                            ),
                            rx.table.cell(rx.text(a["palestrante"], size="2", color="#CBD5E1")),
                            rx.table.cell(
                                rx.hstack(
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="pencil", size=12),
                                            rx.text("Editar", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="1",
                                        variant="surface",
                                        color_scheme="cyan",
                                        on_click=AdminState.abrir_edicao_atividade(a["id"]),
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="trash-2", size=12),
                                            rx.text("Excluir", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="1",
                                        variant="soft",
                                        color_scheme="red",
                                        on_click=AdminState.excluir_atividade(a["id"]),
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    spacing="1",
                                    justify="center",
                                    align="center",
                                ),
                            ),
                            align="center",
                        ),
                    ),
                ),
                width="100%",
                min_width="920px",
                variant="surface",
            ),
            width="100%",
            overflow_x="auto",
            border_radius="12px",
            border="1px solid rgba(255, 255, 255, 0.08)",
            background="rgba(15, 23, 42, 0.6)",
        ),
        spacing="3",
        width="100%",
    )


def seguranca_admin_view() -> rx.Component:
    """Card de segurança e alteração da própria senha do Admin."""
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon(tag="shield-check", size=24, color="#ef4444"),
                rx.vstack(
                    rx.heading("Segurança da Conta Admin", size="4", weight="bold", color="white"),
                    rx.text(
                        "Altere com segurança sua própria credencial de acesso master ao sistema.",
                        size="2",
                        color="#CBD5E1",
                    ),
                    spacing="0",
                    align="start",
                ),
                align="center",
                spacing="2",
            ),
            rx.divider(color_scheme="gray", opacity="0.15"),
            rx.grid(
                rx.vstack(
                    rx.text("Nova Senha do Administrador", size="2", weight="bold", color="white"),
                    rx.input(
                        placeholder="Digite a nova senha (mínimo 6 caracteres)",
                        type="password",
                        value=AdminState.admin_propria_senha_input,
                        on_change=AdminState.set_admin_propria_senha,
                        size="3",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Confirmar Nova Senha", size="2", weight="bold", color="white"),
                    rx.input(
                        placeholder="Repita a nova senha",
                        type="password",
                        value=AdminState.admin_propria_senha_confirm,
                        on_change=AdminState.set_admin_propria_senha_confirm,
                        size="3",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                columns=rx.breakpoints(initial="1", sm="2"),
                spacing="4",
                width="100%",
            ),
            rx.button(
                rx.hstack(
                    rx.icon(tag="lock", size=16),
                    rx.text("Atualizar Minha Senha de Administrador"),
                    spacing="1",
                    align="center",
                ),
                size="3",
                color_scheme="red",
                variant="solid",
                on_click=AdminState.salvar_propria_senha_admin,
                style=STYLE_BUTTON_CHIP,
            ),
            rx.divider(color_scheme="gray", opacity="0.15"),
            # Exportação de Dados e Documentos Oficiais
            rx.vstack(
                rx.heading("Exportação Oficial de Dados e Relatórios", size="3", weight="bold", color="white"),
                rx.text(
                    "Baixe a relação completa de participantes cadastrados no banco SQLite WAL para conferência offline ou impressão.",
                    size="2",
                    color="#CBD5E1",
                ),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="file-spreadsheet", size=16),
                            rx.text("Baixar Planilha (CSV)"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        color_scheme="green",
                        variant="surface",
                        on_click=AdminState.exportar_inscritos_csv,
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="file-down", size=16),
                            rx.text("Baixar Relatório Oficial (PDF)"),
                            spacing="1",
                            align="center",
                        ),
                        size="2",
                        color_scheme="cyan",
                        variant="solid",
                        on_click=AdminState.exportar_inscritos_pdf,
                        style=STYLE_BUTTON_CHIP,
                    ),
                    spacing="3",
                    align="center",
                ),
                spacing="2",
                align="start",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
        padding="1.5rem",
        border_radius="14px",
        background="rgba(15, 23, 42, 0.75)",
        border="1px solid rgba(255, 255, 255, 0.08)",
        width="100%",
    )


def editor_modelos_admin() -> rx.Component:
    """Aba do Administrador para gerenciar os links de download dos modelos acadêmicos."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(tag="file-text", size=22, color=COLOR_CYAN),
                    background="rgba(0, 173, 181, 0.15)",
                    border_radius="10px",
                    padding="0.6rem",
                    display="grid",
                    place_items="center",
                ),
                rx.vstack(
                    rx.heading("Gestão dos Links de Download dos Modelos Acadêmicos", size="4", weight="bold", color="white"),
                    rx.text(
                        "Configure as URLs externas (Google Drive, Dropbox, OneDrive ou institucional) para os modelos oficiais do IV EFAC.",
                        size="2",
                        color="#CBD5E1",
                        style=STYLE_TEXT_RESPONSIVE,
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.divider(color_scheme="gray", opacity="0.2"),
            rx.vstack(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="file-text", size=16, color=COLOR_CYAN),
                        rx.text("1. Modelo de Resumo Expandido (.docx)", size="2", weight="bold", color="white"),
                        rx.badge("Baixar Modelo", color_scheme="cyan", size="1"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text("Link oficial de download do documento de 2 a 4 páginas:", size="1", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_link_resumo_input,
                        on_change=AdminState.set_admin_link_resumo_input,
                        placeholder="https://drive.google.com/file/d/...",
                        size="3",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="presentation", size=16, color="#818CF8"),
                        rx.text("2. Slide para Apresentação Oral (15 min)", size="2", weight="bold", color="white"),
                        rx.badge("Baixar PPTX", color_scheme="blue", size="1"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text("Link oficial do arquivo de slides em formato 16:9:", size="1", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_link_slides_input,
                        on_change=AdminState.set_admin_link_slides_input,
                        placeholder="https://drive.google.com/file/d/...",
                        size="3",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="layout-grid", size=16, color="#34d399"),
                        rx.text("3. Modelo de Pôster / Painel Científico", size="2", weight="bold", color="white"),
                        rx.badge("Baixar Template", color_scheme="green", size="1"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text("Link oficial do template do pôster para dimensões 90x120cm:", size="1", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_link_poster_input,
                        on_change=AdminState.set_admin_link_poster_input,
                        placeholder="https://drive.google.com/file/d/...",
                        size="3",
                        width="100%",
                    ),
                    spacing="1",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            rx.button(
                rx.hstack(
                    rx.icon(tag="save", size=16),
                    rx.text("Salvar e Publicar Links dos Modelos", size="2", weight="bold"),
                    spacing="2",
                    align="center",
                ),
                color_scheme="cyan",
                variant="solid",
                size="3",
                on_click=AdminState.salvar_links_modelos,
                style=STYLE_BUTTON_CHIP,
                width="100%",
                margin_top="0.5rem",
            ),
            spacing="4",
            width="100%",
        ),
        padding="1.75rem",
        background="rgba(15, 23, 42, 0.75)",
        border="1px solid rgba(0, 173, 181, 0.2)",
        border_radius="16px",
        width="100%",
    )


def modal_editar_participante_admin() -> rx.Component:
    """Modal profissional para o administrador editar completamente qualquer perfil de participante."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag="user-cog", size=22, color=COLOR_CYAN),
                        background="rgba(0, 173, 181, 0.15)",
                        border_radius="10px",
                        padding="0.6rem",
                    ),
                    rx.vstack(
                        rx.dialog.title("Edição Completa de Participante", size="4", weight="bold", color="white"),
                        rx.dialog.description(
                            "Altere dados cadastrais, modalidade, eixo temático, privilégios e presença.",
                            size="1",
                            color="#CBD5E1",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                ),
                rx.divider(color_scheme="gray", opacity="0.2"),
                rx.vstack(
                    rx.text("Nome Completo", size="1", weight="bold", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_edit_nome,
                        on_change=AdminState.set_admin_edit_nome,
                        placeholder="Nome completo do participante",
                        size="2",
                        width="100%",
                    ),
                    rx.text("Endereço de E-mail", size="1", weight="bold", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_edit_email,
                        on_change=AdminState.set_admin_edit_email,
                        placeholder="email@instituicao.edu.br",
                        size="2",
                        width="100%",
                    ),
                    rx.text("Instituição de Origem", size="1", weight="bold", color="#CBD5E1"),
                    rx.input(
                        value=AdminState.admin_edit_instituicao,
                        on_change=AdminState.set_admin_edit_instituicao,
                        placeholder="Universidade ou Polo Acadêmico",
                        size="2",
                        width="100%",
                    ),
                    rx.hstack(
                        rx.vstack(
                            rx.text("Modalidade", size="1", weight="bold", color="#CBD5E1"),
                            rx.select(
                                ["Presencial", "Online"],
                                value=AdminState.admin_edit_modalidade,
                                on_change=AdminState.set_admin_edit_modalidade,
                                size="2",
                                width="100%",
                            ),
                            width="50%",
                            spacing="1",
                        ),
                        rx.vstack(
                            rx.text("Privilégio / Função", size="1", weight="bold", color="#CBD5E1"),
                            rx.select(
                                ["participante", "admin"],
                                value=AdminState.admin_edit_role,
                                on_change=AdminState.set_admin_edit_role,
                                size="2",
                                width="100%",
                            ),
                            width="50%",
                            spacing="1",
                        ),
                        width="100%",
                        spacing="3",
                    ),
                    rx.text("Eixo Temático de Interesse", size="1", weight="bold", color="#CBD5E1"),
                    rx.select(
                        [
                            "Astrofísica",
                            "Física Computacional",
                            "Relatividade e Gravitação",
                            "Física Quântica",
                            "Ensino e Divulgação Científica",
                        ],
                        value=AdminState.admin_edit_area,
                        on_change=AdminState.set_admin_edit_area,
                        size="2",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.15"),
                    rx.text("Conferência de Presença Oficial", size="1", weight="bold", color="#CBD5E1"),
                    rx.hstack(
                        rx.hstack(
                            rx.checkbox(
                                checked=AdminState.admin_edit_presenca_d1,
                                on_change=AdminState.toggle_admin_edit_presenca_d1,
                                size="2",
                                color_scheme="cyan",
                            ),
                            rx.text("Presente no Dia 1 (11/Nov)", size="1", color="white"),
                            spacing="2",
                            align="center",
                        ),
                        rx.hstack(
                            rx.checkbox(
                                checked=AdminState.admin_edit_presenca_d2,
                                on_change=AdminState.toggle_admin_edit_presenca_d2,
                                size="2",
                                color_scheme="violet",
                            ),
                            rx.text("Presente no Dia 2 (12/Nov)", size="1", color="white"),
                            spacing="2",
                            align="center",
                        ),
                        width="100%",
                        spacing="4",
                        wrap="wrap",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.hstack(
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="trash-2", size=14),
                            rx.text("Excluir", size="2", weight="bold"),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="red",
                        variant="solid",
                        size="2",
                        on_click=AdminState.excluir_participante_admin,
                        style=STYLE_BUTTON_CHIP,
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            "Cancelar",
                            variant="soft",
                            color_scheme="gray",
                            size="2",
                            on_click=AdminState.fechar_modal_editar_participante,
                            style=STYLE_BUTTON_CHIP,
                        ),
                    ),
                    rx.button(
                        rx.hstack(
                            rx.icon(tag="check", size=14),
                            rx.text("Salvar Alterações", size="2", weight="bold"),
                            spacing="1",
                            align="center",
                        ),
                        color_scheme="cyan",
                        variant="solid",
                        size="2",
                        on_click=AdminState.salvar_edicao_participante,
                        style=STYLE_BUTTON_CHIP,
                    ),
                    spacing="2",
                    align="center",
                    width="100%",
                    margin_top="1rem",
                ),
                spacing="3",
                width="100%",
            ),
            background="rgba(15, 23, 42, 0.98)",
            border="1.5px solid rgba(0, 173, 181, 0.4)",
            border_radius="16px",
            box_shadow="0 20px 60px rgba(0, 0, 0, 0.7)",
            padding="1.75rem",
            max_width="540px",
            width="90vw",
        ),
        open=AdminState.modal_editar_participante_aberto,
    )



def painel_admin_view() -> rx.Component:
    """Componente completo de renderização do Painel de Administração."""
    return rx.box(
        # Modal de alteração de senha de inscrito
        modal_alterar_senha_inscrito(),
        # Modal de visualização de carteirinha de participante
        modal_editar_participante_admin(),

        rx.vstack(
            # Título e Badges
            rx.hstack(
                rx.badge("Acesso Exclusivo Admin", color_scheme="red", variant="solid", size="2"),
                rx.badge("Controle Total do Evento", color_scheme="cyan", variant="soft", size="2"),
                spacing="2",
                align="center",
            ),
            rx.heading("Painel de Controle Administrativo • IV EFAC", size="6", weight="bold", color="white"),
            # Grid de Métricas (4 Indicadores Centrais Otimizados)
            rx.grid(
                stat_metric_box(AdminState.admin_total_inscritos, "Total de Inscritos", "users", "#38bdf8"),
                stat_metric_box(AdminState.admin_total_presenciais, "Vagas Presenciais", "building", "#818cf8"),
                stat_metric_box(AdminState.admin_total_onlines, "Transmissão Online", "globe", "#34d399"),
                stat_metric_box(AdminState.admin_total_presentes, "Presenças Confirmadas", "circle-check", "#f59e0b"),
                columns=rx.breakpoints(initial="2", sm="2", md="4"),
                spacing="3",
                width="100%",
            ),
            # Abas do Admin: Inscritos vs Editor de Grade vs Minha Conta/Segurança
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="users", size=14),
                            rx.text("Participantes Inscritos", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="inscritos",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="calendar", size=14),
                            rx.text("Editor & Delegação de Grade", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="grade",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="shield", size=14),
                            rx.text("Segurança & Minha Senha", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="seguranca",
                    ),
                    rx.tabs.trigger(
                        rx.hstack(
                            rx.icon(tag="file-text", size=14),
                            rx.text("Modelos & Submissões", size="2"),
                            spacing="1",
                            align="center",
                        ),
                        value="modelos",
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
                rx.tabs.content(
                    seguranca_admin_view(),
                    value="seguranca",
                    padding_top="1.5rem",
                ),
                rx.tabs.content(
                    editor_modelos_admin(),
                    value="modelos",
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
        overflow_x="hidden",
        margin_top="1.5rem",
        on_mount=AdminState.carregar_painel_admin,
    )
