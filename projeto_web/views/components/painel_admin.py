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
                on_click=EventoState.fechar_modal_senha,
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
                            rx.text("Redefinição direta no banco SQLite WAL", size="1", color="var(--gray-9)"),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.icon(tag="x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            size="1",
                            on_click=EventoState.fechar_modal_senha,
                            cursor="pointer",
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.2"),
                    rx.box(
                        rx.hstack(
                            rx.icon(tag="user", size=16, color="var(--gray-10)"),
                            rx.text(
                                "Participante: ",
                                rx.text.strong(AdminState.admin_senha_user_nome, color="white"),
                                size="2",
                                color="var(--gray-10)",
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
                            on_click=EventoState.fechar_modal_senha,
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


def modal_carteirinha_admin() -> rx.Component:
    """Modal para o administrador visualizar, conferir e imprimir a carteirinha de qualquer inscrito."""
    return rx.cond(
        AdminState.admin_carteirinha_aberta,
        rx.box(
            # Backdrop de foco
            rx.box(
                position="fixed",
                inset="0",
                background="rgba(0, 0, 0, 0.85)",
                z_index="1000",
                backdrop_filter="blur(8px)",
                on_click=AdminState.fechar_carteirinha_admin,
            ),
            # Caixa do Modal
            rx.card(
                rx.vstack(
                    rx.hstack(
                        rx.box(
                            rx.icon(tag="id-card", size=22, color=COLOR_CYAN),
                            background="rgba(0, 173, 181, 0.15)",
                            border_radius="8px",
                            padding="0.5rem",
                            display="grid",
                            place_items="center",
                        ),
                        rx.vstack(
                            rx.heading("Carteirinha Oficial do Participante", size="4", weight="bold", color="white"),
                            rx.text("Emissão digital com chancela acadêmica UFCA / IFE", size="1", color="var(--gray-9)"),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="download", size=14),
                                rx.text("Baixar Imagem (PNG)"),
                                spacing="1",
                                align="center",
                            ),
                            size="1",
                            variant="solid",
                            color_scheme="cyan",
                            on_click=AdminState.baixar_carteirinha_admin_png,
                            style=STYLE_BUTTON_CHIP,
                        ),
                        rx.button(
                            rx.icon(tag="x", size=18),
                            variant="ghost",
                            color_scheme="gray",
                            size="1",
                            on_click=AdminState.fechar_carteirinha_admin,
                            cursor="pointer",
                        ),
                        align="center",
                        width="100%",
                    ),
                    rx.divider(color_scheme="gray", opacity="0.2"),
                    # Cartão de Identificação / Carteirinha
                    rx.box(
                        rx.vstack(
                            rx.hstack(
                                rx.image(
                                    src="/logo_ivefac.jpeg",
                                    alt="Logo IV EFAC",
                                    width="36px",
                                    height="36px",
                                    border_radius="50%",
                                    object_fit="cover",
                                    border="1.5px solid #00ADB5",
                                ),
                                rx.vstack(
                                    rx.text("IV EFAC 2026", size="2", weight="bold", color="white"),
                                    rx.text("Universidade Federal do Cariri • Campus Brejo Santo", size="1", color="var(--gray-9)"),
                                    spacing="0",
                                ),
                                rx.spacer(),
                                rx.badge("CARTEIRINHA OFICIAL", color_scheme="cyan", variant="solid", size="1"),
                                align="center",
                                width="100%",
                            ),
                            rx.divider(color_scheme="cyan", opacity="0.3"),
                            rx.hstack(
                                rx.box(
                                    rx.cond(
                                        AdminState.admin_carteirinha_foto != "",
                                        rx.image(
                                            src=AdminState.admin_carteirinha_foto,
                                            alt=AdminState.admin_carteirinha_nome,
                                            width="95px",
                                            height="95px",
                                            border_radius="50%",
                                            object_fit="cover",
                                            border="2.5px solid #00ADB5",
                                            box_shadow="0 0 16px rgba(0, 173, 181, 0.4)",
                                        ),
                                        rx.image(
                                            src="/favicon.png",
                                            alt="Soldadinho do Araripe",
                                            width="95px",
                                            height="95px",
                                            border_radius="50%",
                                            object_fit="cover",
                                            border="2.5px solid #00ADB5",
                                            box_shadow="0 0 16px rgba(0, 173, 181, 0.4)",
                                        ),
                                    ),
                                    display="grid",
                                    place_items="center",
                                ),
                                rx.vstack(
                                    rx.text(AdminState.admin_carteirinha_nome, size="3", weight="bold", color="white"),
                                    rx.text(AdminState.admin_carteirinha_email, size="1", color="var(--gray-10)"),
                                    rx.text(AdminState.admin_carteirinha_inst, size="1", color="var(--gray-9)"),
                                    rx.hstack(
                                        rx.badge(AdminState.admin_carteirinha_mod, color_scheme="indigo", size="1"),
                                        rx.badge(AdminState.admin_carteirinha_role.upper(), color_scheme="violet", size="1"),
                                        rx.badge(
                                            rx.hstack(
                                                rx.icon(tag="qr-code", size=11),
                                                rx.text(AdminState.admin_carteirinha_cod, size="1"),
                                                spacing="1",
                                                align="center",
                                            ),
                                            color_scheme="cyan",
                                            variant="surface",
                                            size="1",
                                        ),
                                        spacing="2",
                                        wrap="wrap",
                                    ),
                                    spacing="1",
                                    align="start",
                                    flex="1",
                                ),
                                spacing="3",
                                align="center",
                                width="100%",
                            ),
                            rx.box(
                                rx.hstack(
                                    rx.hstack(
                                        rx.icon(tag="calendar", size=13, color="#00ADB5"),
                                        rx.text("11 e 12 Nov 2026", size="1", weight="bold", color="white"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    rx.hstack(
                                        rx.icon(tag="clock", size=13, color="#f59e0b"),
                                        rx.text("08h00 Abertura", size="1", weight="bold", color="white"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    rx.spacer(),
                                    rx.text("Fomento FUNCAP", size="1", color="#38bdf8"),
                                    align="center",
                                    width="100%",
                                ),
                                padding="0.55rem 0.85rem",
                                background="rgba(0, 0, 0, 0.4)",
                                border_radius="10px",
                                border="1px solid rgba(255, 255, 255, 0.08)",
                                width="100%",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        padding="1.35rem",
                        background="linear-gradient(155deg, rgba(8, 12, 28, 0.98) 0%, rgba(16, 28, 54, 0.95) 100%)",
                        border="1.5px solid rgba(0, 173, 181, 0.5)",
                        border_radius="16px",
                        box_shadow="0 10px 35px rgba(0, 173, 181, 0.25)",
                        width="100%",
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
                max_width="560px",
                background="rgba(15, 23, 42, 0.98)",
                border="1.5px solid rgba(0, 173, 181, 0.4)",
                box_shadow="0 25px 60px rgba(0, 0, 0, 0.85)",
                border_radius="16px",
                padding="1.5rem",
            ),
        ),
        rx.fragment(),
    )


def tabela_inscritos_admin() -> rx.Component:
    """Tabela analítica de participantes com alteração de senha, emissão de carteirinha e exportação em CSV/PDF."""
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
            ),
            width="100%",
            spacing="2",
            wrap="wrap",
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
                        rx.table.column_header_cell("Ações Administrativas"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        AdminState.admin_inscritos,
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
                                    rx.badge("Admin", color_scheme="red", variant="solid", size="1"),
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
                                rx.hstack(
                                    # Botão Carteirinha
                                    rx.button(
                                        rx.hstack(
                                            rx.icon(tag="id-card", size=12),
                                            rx.text("Carteirinha", size="1"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        size="1",
                                        variant="outline",
                                        color_scheme="cyan",
                                        on_click=AdminState.ver_carteirinha_admin(u["id"]),
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    rx.cond(
                                        u["role"] != "admin",
                                        rx.cond(
                                            u["is_supervisor"],
                                            rx.button(
                                                "Revogar",
                                                size="1",
                                                variant="outline",
                                                color_scheme="red",
                                                on_click=EventoState.rebaixar_supervisor(u["id"]),
                                                style=STYLE_BUTTON_CHIP,
                                            ),
                                            rx.button(
                                                "Supervisor",
                                                size="1",
                                                variant="solid",
                                                color_scheme="violet",
                                                on_click=EventoState.promover_supervisor(u["id"]),
                                                style=STYLE_BUTTON_CHIP,
                                            ),
                                        ),
                                        rx.badge("Master", color_scheme="red", variant="soft", size="1"),
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
                                        on_click=EventoState.abrir_modal_senha(u["id"], u["nome"]),
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    spacing="2",
                                    align="center",
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
    """Editor completo de palestras, delegação de responsáveis, temas e horários da grade oficial."""
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.heading("Gestão e Delegação Manual da Grade de Atividades", size="4", weight="bold", color="white"),
                rx.text(
                    "Altere manualmente datas, horários e temas, delegue responsáveis e crie novas atividades diretamente pelo site.",
                    size="2",
                    color="var(--gray-10)",
                ),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.hstack(
                # Botão Criar / Delegar Nova Atividade
                rx.button(
                    rx.hstack(
                        rx.icon(tag="plus-circle", size=14),
                        rx.text("Delegar Nova Atividade", size="1"),
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
                        rx.icon(tag="plus-circle", size=18, color=COLOR_CYAN),
                        rx.heading("Delegar e Criar Nova Atividade na Grade", size="3", weight="bold", color="white"),
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
                            rx.text("Horário / Faixa Horária (Manual)", size="1", weight="bold", color="white"),
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
                            rx.text("Horário / Faixa Horária (Manual)", size="1", weight="bold", color="white"),
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
                        rx.table.column_header_cell("Dia"),
                        rx.table.column_header_cell("Horário"),
                        rx.table.column_header_cell("Tipo"),
                        rx.table.column_header_cell("Tema / Atividade"),
                        rx.table.column_header_cell("Responsável Delegado"),
                        rx.table.column_header_cell("Ação"),
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
                                    rx.text(a["local"], size="1", color="var(--gray-9)"),
                                    spacing="0",
                                ),
                            ),
                            rx.table.cell(rx.text(a["palestrante"], size="2", color="var(--gray-11)")),
                            rx.table.cell(
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
                        color="var(--gray-10)",
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
                    color="var(--gray-10)",
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


def painel_admin_view() -> rx.Component:
    """Componente completo de renderização do Painel de Administração."""
    return rx.box(
        # Modal de alteração de senha de inscrito
        modal_alterar_senha_inscrito(),
        # Modal de visualização de carteirinha de participante
        modal_carteirinha_admin(),

        rx.vstack(
            # Título e Badges
            rx.hstack(
                rx.badge("Acesso Exclusivo Admin", color_scheme="red", variant="solid", size="2"),
                rx.badge("Controle Total do Evento", color_scheme="cyan", variant="soft", size="2"),
                spacing="2",
                align="center",
            ),
            rx.heading("Painel de Controle Administrativo • IV EFAC", size="6", weight="bold", color="white"),
            # Grid de Métricas
            rx.grid(
                stat_metric_box(AdminState.admin_total_inscritos, "Total de Inscritos", "users", "#38bdf8"),
                stat_metric_box(AdminState.admin_total_presenciais, "Vagas Presenciais", "building", "#818cf8"),
                stat_metric_box(AdminState.admin_total_onlines, "Transmissão Online", "globe", "#34d399"),
                stat_metric_box(AdminState.admin_total_presentes, "Presenças Confirmadas", "check-circle", "#f59e0b"),
                stat_metric_box(AdminState.admin_total_supervisores, "Supervisores Ativos", "shield", "#c084fc"),
                columns=rx.breakpoints(initial="2", sm="3", md="5"),
                spacing="3",
                width="100%",
            ),
            # Abas do Admin: Inscritos vs Editor de Grade vs Minha Conta/Segurança
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
        on_mount=AdminState.carregar_painel_admin,
    )
