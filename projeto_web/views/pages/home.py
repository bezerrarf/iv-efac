"""Página Inicial do IV EFAC: Portal de Física Contemporânea e Computação Científica (View).
Arquitetura de Tela Única com navegação de seções integrada diretamente ao topo (Navbar).
Estética de alto desempenho com malha gravitacional em tempo real e visual de centro de pesquisas.
"""

import reflex as rx
from datetime import datetime
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.footer import parceiro_chip
from projeto_web.views.components.space_fabric import space_fabric_canvas
from projeto_web.controllers.evento_controller import (
    EventoController,
    EixoTematico,
    Palestrante,
    Atividade,
)
from projeto_web.state.evento_state import EventoState


def logo_orbital_hpc() -> rx.Component:
    """Logotipo orbital de alta tecnologia com efeito de lente gravitacional."""
    return rx.box(
        # Halo de distorção cósmica
        rx.box(
            position="absolute",
            inset="-25px",
            border_radius="50%",
            background=rx.color_mode_cond(
                light="radial-gradient(circle, rgba(16, 52, 96, 0.2) 0%, rgba(0, 173, 181, 0.12) 55%, transparent 75%)",
                dark="radial-gradient(circle, rgba(0, 173, 181, 0.3) 0%, rgba(99, 102, 241, 0.2) 50%, transparent 75%)",
            ),
            filter="blur(22px)",
            z_index="1",
        ),
        # Órbita Relativística 1 (Tracejada com brilho)
        rx.box(
            position="absolute",
            inset="6px",
            border_radius="50%",
            border=rx.color_mode_cond(
                light="1.5px dashed rgba(16, 52, 96, 0.4)",
                dark="1.5px dashed rgba(0, 173, 181, 0.5)",
            ),
            transform="rotate(-28deg)",
            z_index="2",
        ),
        # Órbita Relativística 2 (Contínua)
        rx.box(
            position="absolute",
            inset="22px",
            border_radius="50%",
            border=rx.color_mode_cond(
                light="1.5px solid rgba(0, 173, 181, 0.4)",
                dark="1.5px solid rgba(129, 140, 248, 0.45)",
            ),
            transform="rotate(38deg)",
            z_index="2",
        ),
        # Ponto Quântico / Partícula
        rx.box(
            position="absolute",
            top="14px",
            right="28px",
            width="8px",
            height="8px",
            border_radius="50%",
            background=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"),
            box_shadow=rx.color_mode_cond(
                light="0 0 10px #00ADB5",
                dark="0 0 12px #38bdf8, 0 0 4px #ffffff",
            ),
            z_index="3",
        ),
        # Núcleo do Evento (Singularidade / Anã Branca)
        rx.box(
            rx.vstack(
                rx.icon(
                    tag="telescope",
                    size=42,
                    color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                ),
                rx.text(
                    "IV EFAC",
                    size="3",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="white"),
                    letter_spacing="2.5px",
                ),
                rx.badge("2026", color_scheme="cyan", variant="soft", size="1"),
                spacing="1",
                align="center",
            ),
            width="135px",
            height="135px",
            border_radius="50%",
            background=rx.color_mode_cond(
                light="linear-gradient(145deg, #ffffff 10%, #f1f5f9 100%)",
                dark="linear-gradient(145deg, #090e1f 10%, #103460 100%)",
            ),
            border=rx.color_mode_cond(
                light="3px solid #103460",
                dark="3px solid rgba(0, 173, 181, 0.7)",
            ),
            box_shadow=rx.color_mode_cond(
                light="0 10px 30px rgba(16, 52, 96, 0.2)",
                dark="0 0 35px rgba(0, 173, 181, 0.4), inset 0 0 20px rgba(16, 52, 96, 0.6)",
            ),
            display="grid",
            place_items="center",
            position="relative",
            z_index="4",
        ),
        width="200px",
        height="200px",
        display="grid",
        place_items="center",
        position="relative",
        margin="0 auto",
    )


def display_hud_contagem() -> rx.Component:
    """Display digital estilo relógio atômico para o início do simpósio."""
    alvo = datetime(2026, 11, 11, 8, 0, 0)
    agora = datetime(2026, 10, 1, 16, 0, 0)
    dias = max((alvo - agora).days, 0)
    horas = max(((alvo - agora).seconds // 3600), 0)

    def hud_item(val: str, label: str) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.heading(val, size="5", weight="bold", color=rx.color_mode_cond(light="#103460", dark="#00ADB5")),
                rx.text(label, size="1", color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)"), text_transform="uppercase"),
                spacing="0",
                align="center",
            ),
            background=rx.color_mode_cond(light="rgba(255, 255, 255, 0.9)", dark="rgba(15, 23, 42, 0.75)"),
            border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(0, 173, 181, 0.25)"),
            border_radius="10px",
            padding="0.45rem 0.85rem",
            min_width="65px",
            box_shadow="0 2px 8px rgba(0, 0, 0, 0.05)",
        )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="6px",
                    height="6px",
                    border_radius="50%",
                    background="#00ADB5",
                    box_shadow="0 0 8px #00ADB5",
                ),
                rx.text(
                    "CONTAGEM REGRESSIVA PARA ABERTURA",
                    size="1",
                    weight="bold",
                    letter_spacing="1.5px",
                    color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                ),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                hud_item(str(dias), "Dias"),
                hud_item(str(horas), "Horas"),
                hud_item("30", "Min"),
                hud_item("00", "Seg"),
                spacing="2",
                align="center",
            ),
            spacing="1",
            align="start",
        ),
    )


# --- 1. TELA INÍCIO: COCKPIT CIENTÍFICO ---

def tela_inicio() -> rx.Component:
    stats = EventoController.STATS

    return rx.box(
        rx.hstack(
            # Coluna de Texto e Informações Principais
            rx.vstack(
                rx.badge(
                    rx.hstack(
                        rx.box(
                            width="6px",
                            height="6px",
                            border_radius="50%",
                            background="#34d399",
                            box_shadow="0 0 6px #34d399",
                        ),
                        rx.text("11 e 12 de Novembro de 2026 • Campus Brejo Santo – UFCA"),
                        spacing="2",
                        align="center",
                    ),
                    color_scheme="cyan",
                    variant="surface",
                    size="2",
                    padding_x="0.8rem",
                ),
                rx.heading(
                    "IV Encontro de Física e Astronomia do Cariri",
                    size="8",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="white"),
                    line_height="1.15",
                ),
                rx.text(
                    "Fronteiras da Física Contemporânea, Formação Científica e Integração Regional",
                    size="4",
                    weight="medium",
                    color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"),
                ),
                rx.text(
                    "Convergência de Astrofísica Relativística, Relatividade Geral, "
                    "Computação de Alto Desempenho (HPC) e Ensino de Ciências no interior do Ceará.",
                    size="3",
                    color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    line_height="1.6",
                    max_width="620px",
                ),
                # Display HUD de Contagem
                display_hud_contagem(),
                # Ações de Alto Impacto
                rx.hstack(
                    rx.link(
                        rx.button(
                            rx.hstack(
                                rx.text("Garantir Minha Inscrição"),
                                rx.icon(tag="arrow-right", size=16),
                                spacing="1",
                                align="center",
                            ),
                            size="3",
                            radius="full",
                            padding_x="1.8rem",
                            font_weight="bold",
                            background="#103460",
                            color="white",
                            box_shadow="0 6px 20px rgba(16, 52, 96, 0.35)",
                            _hover={"transform": "translateY(-1px)", "background": "#16457e"},
                            transition="all 0.2s ease",
                        ),
                        href="/inscricao",
                    ),
                    rx.button(
                        rx.hstack(
                            rx.text("Submeter Trabalho"),
                            rx.icon(tag="file-text", size=16),
                            spacing="1",
                            align="center",
                        ),
                        size="3",
                        variant="outline",
                        color_scheme="cyan",
                        radius="full",
                        padding_x="1.6rem",
                        font_weight="bold",
                        border=rx.color_mode_cond(light="1.5px solid #00ADB5", dark="1.5px solid #00ADB5"),
                        color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                        on_click=lambda: EventoState.set_tela("submissoes"),
                    ),
                    spacing="3",
                    margin_top="0.5rem",
                    wrap="wrap",
                ),
                align="start",
                spacing="4",
                max_width="660px",
            ),
            # Coluna de Destaque Orbital + Telemetria HPC
            rx.vstack(
                logo_orbital_hpc(),
                # Painel de Telemetria Científica
                rx.grid(
                    *[
                        rx.box(
                            rx.vstack(
                                rx.heading(s["valor"], size="6", weight="bold", color=rx.color_mode_cond(light="#103460", dark="#00ADB5")),
                                rx.text(s["rotulo"], size="1", color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"), text_align="center"),
                                spacing="0",
                                align="center",
                            ),
                            background=rx.color_mode_cond(light="rgba(255, 255, 255, 0.88)", dark="rgba(15, 23, 42, 0.75)"),
                            backdrop_filter="blur(10px)",
                            border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(0, 173, 181, 0.25)"),
                            border_radius="14px",
                            padding="0.8rem 1rem",
                            text_align="center",
                            box_shadow="0 4px 15px rgba(0, 0, 0, 0.05)",
                        )
                        for s in stats
                    ],
                    columns="2",
                    spacing="3",
                    width="100%",
                    max_width="380px",
                    margin_top="1rem",
                ),
                align="center",
                spacing="3",
            ),
            justify="between",
            align="center",
            spacing="7",
            wrap="wrap",
            width="100%",
            max_width="1220px",
            margin="0 auto",
            padding_y="2rem",
        ),
        width="100%",
    )


# --- 2. TELA SOBRE: HISTÓRICO BINGO & FOMENTO ---

def tela_sobre() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.badge("Origens & Cooperação Internacional", color_scheme="cyan", variant="soft", size="2"),
            rx.heading(
                "Sobre o Encontro & Consolidação Regional",
                size="8",
                weight="bold",
                color=rx.color_mode_cond(light="#103460", dark="white"),
                text_align="center",
            ),
            rx.text(
                "Desde 2019, o EFAC é a principal plataforma de integração entre a pesquisa "
                "de ponta em física relativística e a formação de cientistas e educadores no interior cearense.",
                size="3",
                color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                text_align="center",
                max_width="760px",
            ),
            rx.grid(
                # Card Radiotelescópio BINGO
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="radio", size=24, color="#103460"),
                            rx.heading("Acordo UFCA-USP & Radiotelescópio BINGO", size="4", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "O pioneirismo do encontro nasceu associado à colaboração científica no "
                            "projeto do Radiotelescópio BINGO (Baryon Acoustic Oscillations in Neutral Gas Observations), "
                            "conectando o Cariri à cosmologia observacional de classe mundial.",
                            size="2",
                            color=rx.color_mode_cond(light="#334155", dark="var(--gray-11)"),
                            line_height="1.6",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.6rem",
                    border_radius="16px",
                ),
                # Card Fomento Oficial FUNCAP
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="award", size=24, color="#00ADB5"),
                            rx.heading("Fomento Oficial FUNCAP • Governo do Ceará", size="4", weight="bold"),
                            spacing="2",
                            align="center",
                        ),
                        rx.text(
                            "Financiado sob o Edital 03/2026 de Apoio a Eventos Científicos "
                            "(Processo: CER-0264-00190.01.00/26), o IV EFAC viabiliza a interiorização "
                            "efetiva da pós-graduação e iniciação científica no IFE – Campus Brejo Santo.",
                            size="2",
                            color=rx.color_mode_cond(light="#334155", dark="var(--gray-11)"),
                            line_height="1.6",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.6rem",
                    border_radius="16px",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="5",
                max_width="1060px",
                width="100%",
                margin_top="1rem",
            ),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.text("Explorar os 4 Eixos Temáticos"),
                        rx.icon(tag="arrow-right", size=16),
                        spacing="1",
                        align="center",
                    ),
                    size="3",
                    radius="full",
                    background="#103460",
                    color="white",
                    on_click=lambda: EventoState.set_tela("eixos"),
                ),
                margin_top="1.5rem",
            ),
            spacing="4",
            align="center",
            justify="center",
            width="100%",
            max_width="1200px",
            margin="0 auto",
            padding_y="2rem",
        ),
        width="100%",
    )


# --- 3. TELA EIXOS: MATRIZ DE PESQUISA HPC ---

def tela_eixos() -> rx.Component:
    eixos = EventoController.obter_eixos_tematicos()

    def card_eixo_hpc(e: EixoTematico) -> rx.Component:
        return rx.card(
            rx.vstack(
                rx.hstack(
                    rx.box(
                        rx.icon(tag=e.icone, size=22, color=e.cor),
                        padding="0.6rem",
                        border_radius="12px",
                        background=f"{e.cor}18",
                    ),
                    rx.badge(f"Eixo {e.numero}", color_scheme="cyan", variant="surface", size="2"),
                    spacing="2",
                    align="center",
                ),
                rx.heading(e.titulo, size="4", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
                rx.text(e.subtitulo, size="2", weight="medium", color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8")),
                rx.text(e.descricao, size="2", color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"), line_height="1.5"),
                rx.divider(),
                rx.hstack(
                    *[rx.badge(t, size="1", variant="outline") for t in e.tags],
                    spacing="1",
                    wrap="wrap",
                ),
                spacing="3",
                align="start",
            ),
            padding="1.5rem",
            border_radius="16px",
            height="100%",
            _hover={"transform": "translateY(-4px)", "border_color": e.cor},
            transition="all 0.22s ease",
        )

    return rx.box(
        rx.vstack(
            rx.badge("Matriz Interdisciplinar", color_scheme="cyan", variant="soft", size="2"),
            rx.heading("Eixos Temáticos do Encontro", size="8", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.text(
                "Estrutura temática para apresentação de artigos, resumos expandidos e mesas de debate.",
                size="3",
                color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                text_align="center",
            ),
            rx.grid(
                *[card_eixo_hpc(e) for e in eixos],
                columns=rx.breakpoints(initial="1", sm="2", lg="4"),
                spacing="4",
                max_width="1240px",
                width="100%",
                margin_top="1rem",
            ),
            rx.button(
                rx.hstack(
                    rx.text("Conhecer os Palestrantes Destas Áreas"),
                    rx.icon(tag="arrow-right", size=16),
                    spacing="1",
                    align="center",
                ),
                size="3",
                radius="full",
                background="#103460",
                color="white",
                margin_top="1.5rem",
                on_click=lambda: EventoState.set_tela("palestrantes"),
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        width="100%",
    )


# --- 4. TELA PALESTRANTES: KEYNOTES SUMMIT ---

def tela_palestrantes() -> rx.Component:
    palestrantes = EventoController.obter_palestrantes()

    def keynote_card_hpc(p: Palestrante) -> rx.Component:
        return rx.card(
            rx.vstack(
                rx.avatar(
                    fallback=p.nome[6:8].upper() if len(p.nome) > 8 else p.nome[:2].upper(),
                    size="4",
                    radius="full",
                    color_scheme="cyan",
                ),
                rx.heading(p.nome, size="3", weight="bold", text_align="center", color=rx.color_mode_cond(light="#103460", dark="white")),
                rx.text(p.cargo, size="1", color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8"), text_align="center"),
                rx.badge(p.instituicao, size="1", variant="soft", color_scheme="indigo"),
                rx.text(
                    p.especialidade,
                    size="1",
                    color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                    text_align="center",
                    line_height="1.4",
                ),
                spacing="1",
                align="center",
            ),
            padding="1.2rem",
            width="100%",
            border_radius="14px",
            _hover={"transform": "translateY(-3px)"},
            transition="all 0.2s ease",
        )

    return rx.box(
        rx.vstack(
            rx.badge("Quadro Técnico Internacional & Nacional", color_scheme="indigo", variant="soft", size="2"),
            rx.heading("Palestrantes Convidados (Keynotes)", size="8", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.text(
                "Pesquisadores líderes do ITA (São José dos Campos), CBPF, UFRGS, UFPB, IFCE e UECE.",
                size="3",
                color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                text_align="center",
            ),
            rx.grid(
                *[keynote_card_hpc(p) for p in palestrantes],
                columns=rx.breakpoints(initial="1", sm="2", md="3", lg="4"),
                spacing="3",
                max_width="1220px",
                width="100%",
                margin_top="1rem",
            ),
            rx.button(
                rx.hstack(
                    rx.text("Conferir a Grade Horária"),
                    rx.icon(tag="arrow-right", size=16),
                    spacing="1",
                    align="center",
                ),
                size="3",
                radius="full",
                background="#103460",
                color="white",
                margin_top="1.5rem",
                on_click=lambda: EventoState.set_tela("programacao"),
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        width="100%",
    )


# --- 5. TELA PROGRAMAÇÃO: TERMINAL DE GRADE ---

def tela_programacao() -> rx.Component:
    dia1 = EventoController.obter_programacao("Dia 1")
    dia2 = EventoController.obter_programacao("Dia 2")

    def schedule_item_hpc(item: Atividade) -> rx.Component:
        return rx.card(
            rx.hstack(
                rx.badge(item.horario, color_scheme="cyan", variant="solid", size="1"),
                rx.vstack(
                    rx.hstack(
                        rx.badge(item.tipo, color_scheme=item.tipo_color, size="1", variant="soft"),
                        rx.text(item.local, size="1", color="var(--gray-9)"),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(item.titulo, size="2", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
                    rx.text(item.palestrante, size="1", color=rx.color_mode_cond(light="#00ADB5", dark="#38bdf8")),
                    spacing="0",
                    align="start",
                    width="100%",
                ),
                align="start",
                spacing="3",
                width="100%",
            ),
            padding="0.85rem",
            width="100%",
            margin_bottom="0.4rem",
            border_radius="12px",
        )

    return rx.box(
        rx.vstack(
            rx.badge("Grade Oficial • 2 Dias", color_scheme="cyan", variant="soft", size="2"),
            rx.heading("Programação do Simpósio", size="8", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.hstack(
                rx.button(
                    "Dia 1 • 11/Nov (Quarta-feira)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 1", "solid", "outline"),
                    color_scheme="indigo",
                    on_click=lambda: EventoState.set_dia("Dia 1"),
                    radius="full",
                    size="2",
                    padding_x="1.4rem",
                    background=rx.cond(EventoState.dia_selecionado == "Dia 1", "#103460", "transparent"),
                ),
                rx.button(
                    "Dia 2 • 12/Nov (Quinta-feira)",
                    variant=rx.cond(EventoState.dia_selecionado == "Dia 2", "solid", "outline"),
                    color_scheme="indigo",
                    on_click=lambda: EventoState.set_dia("Dia 2"),
                    radius="full",
                    size="2",
                    padding_x="1.4rem",
                    background=rx.cond(EventoState.dia_selecionado == "Dia 2", "#103460", "transparent"),
                ),
                spacing="3",
            ),
            rx.box(
                rx.cond(
                    EventoState.dia_selecionado == "Dia 1",
                    rx.vstack(*[schedule_item_hpc(item) for item in dia1]),
                    rx.vstack(*[schedule_item_hpc(item) for item in dia2]),
                ),
                width="100%",
                max_width="860px",
                max_height="420px",
                overflow_y="auto",
            ),
            rx.hstack(
                rx.link(
                    rx.button(
                        "Abrir Grade Expandida Completa",
                        variant="outline",
                        color_scheme="cyan",
                        size="2",
                        radius="full",
                    ),
                    href="/cronograma",
                ),
                rx.button(
                    rx.hstack(
                        rx.text("Ver Regras de Submissão"),
                        rx.icon(tag="arrow-right", size=15),
                        spacing="1",
                        align="center",
                    ),
                    size="2",
                    radius="full",
                    background="#103460",
                    color="white",
                    on_click=lambda: EventoState.set_tela("submissoes"),
                ),
                spacing="3",
                margin_top="0.8rem",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        width="100%",
    )


# --- 6. TELA SUBMISSÕES: DIRETRIZES & ANAIS ---

def tela_submissoes() -> rx.Component:
    normas = EventoController.obter_normas_submissao()

    return rx.box(
        rx.vstack(
            rx.badge("Publicação Oficial nos Anais", color_scheme="indigo", variant="soft", size="2"),
            rx.heading("Chamada de Trabalhos (Submissões)", size="8", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.text(
                "Submeta seu resumo expandido para publicação nos Anais oficiais do IV EFAC.",
                size="3",
                color=rx.color_mode_cond(light="#475569", dark="var(--gray-10)"),
                text_align="center",
            ),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.heading("Diretrizes de Envio", size="3", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
                        rx.divider(),
                        rx.text(f"• Formato: {normas.formato}", size="2"),
                        rx.text(f"• Extensão: {normas.paginas}", size="2"),
                        rx.text(f"• Modalidades: {normas.modalidade}", size="2"),
                        rx.text(f"• Publicação: {normas.publicacao}", size="2"),
                        spacing="2",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Critérios da Comissão", size="3", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
                        rx.divider(),
                        *[
                            rx.hstack(
                                rx.icon(tag="circle-check", size=16, color="#059669"),
                                rx.text(crit, size="2"),
                                spacing="2",
                                align="center",
                            )
                            for crit in normas.criterios
                        ],
                        spacing="1",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                max_width="920px",
                width="100%",
                margin_top="0.8rem",
            ),
            rx.link(
                rx.button(
                    rx.hstack(
                        rx.icon(tag="upload", size=16),
                        rx.text("Acessar Área do Participante para Submeter"),
                        spacing="2",
                        align="center",
                    ),
                    size="3",
                    radius="full",
                    padding_x="2rem",
                    font_weight="bold",
                    background="#103460",
                    color="white",
                    _hover={"background": "#16457e"},
                ),
                href="/inscricao",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1.5rem",
        ),
        width="100%",
    )


# --- 7. TELA LOCAL & INSCRIÇÃO: COORDENADAS & CREDENCIAIS ---

def tela_local() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.badge("Deslocamento & Credenciamento", color_scheme="cyan", variant="soft", size="2"),
            rx.heading("Localização & Inscrições", size="8", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
            rx.grid(
                rx.card(
                    rx.vstack(
                        rx.hstack(
                            rx.icon(tag="map-pin", size=22, color="#00ADB5"),
                            rx.vstack(
                                rx.heading("Universidade Federal do Cariri (UFCA)", size="3", weight="bold"),
                                rx.text("Instituto de Formação de Educadores – IFE • Campus Brejo Santo", size="2"),
                                rx.text("Rua Olegário Emídio de Araújo, s/n - Centro, Brejo Santo - CE • CEP 63260-000", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="3",
                            align="start",
                            width="100%",
                        ),
                        rx.divider(),
                        rx.hstack(
                            rx.hstack(
                                rx.icon(tag="plane", size=16, color="#103460"),
                                rx.text("Aeroporto de Juazeiro do Norte (JDO) a ~65 km", size="1"),
                                spacing="1",
                            ),
                            rx.hstack(
                                rx.icon(tag="bus", size=16, color="#103460"),
                                rx.text("Acesso pelas rodovias BR-116 e CE-397", size="1"),
                                spacing="1",
                            ),
                            spacing="3",
                            wrap="wrap",
                        ),
                        spacing="2",
                        align="start",
                        width="100%",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    width="100%",
                ),
                # Card de Inscrição Direta
                rx.card(
                    rx.vstack(
                        rx.heading("Garanta sua Vaga Gratuita no IV EFAC", size="4", weight="bold", color=rx.color_mode_cond(light="#103460", dark="white")),
                        rx.text("Inscrição presencial no Campus Brejo Santo ou com acesso à transmissão global e certificação.", size="2", color="var(--gray-10)"),
                        rx.link(
                            rx.button(
                                "Fazer Inscrição Agora",
                                size="3",
                                radius="full",
                                padding_x="1.8rem",
                                background="#103460",
                                color="white",
                                _hover={"background": "#16457e"},
                            ),
                            href="/inscricao",
                        ),
                        spacing="3",
                        align="start",
                    ),
                    padding="1.5rem",
                    border_radius="16px",
                    width="100%",
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                max_width="1000px",
                width="100%",
            ),
            # Régua de Parceiros e Fomento
            rx.flex(
                parceiro_chip("FUNCAP", "Edital 03/2026"),
                parceiro_chip("Governo do Ceará", "Fomento Oficial"),
                parceiro_chip("UFCA / IFE", "Campus Brejo Santo"),
                parceiro_chip("ITA", "São José dos Campos"),
                parceiro_chip("CBPF", "Rio de Janeiro"),
                parceiro_chip("UFRGS", "Porto Alegre"),
                parceiro_chip("UFPB", "João Pessoa"),
                parceiro_chip("IFCE", "Ceará"),
                parceiro_chip("UECE", "Ceará"),
                parceiro_chip("URCA", "Cariri"),
                parceiro_chip("Observatório Kariri", "Divulgação"),
                gap="2",
                wrap="wrap",
                justify="center",
                max_width="920px",
                margin_top="0.8rem",
            ),
            spacing="3",
            align="center",
            justify="center",
            width="100%",
            max_width="1280px",
            margin="0 auto",
            padding_y="1rem",
        ),
        width="100%",
    )


# --- PÁGINA PRINCIPAL HOME: STAGE DE TELA ÚNICA ---

def home_page() -> rx.Component:
    return rx.box(
        # Topo com navegação integrada de seções
        navbar(),

        # Fundo dinâmico com malha do tecido espacial reativa ao mouse/toque
        space_fabric_canvas(),

        # Palco Central de Tela Única
        rx.box(
            rx.cond(
                EventoState.tela_ativa == "inicio",
                tela_inicio(),
                rx.cond(
                    EventoState.tela_ativa == "eixos",
                    tela_eixos(),
                    rx.cond(
                        EventoState.tela_ativa == "palestrantes",
                        tela_palestrantes(),
                        rx.cond(
                            EventoState.tela_ativa == "programacao",
                            tela_programacao(),
                            rx.cond(
                                EventoState.tela_ativa == "submissoes",
                                tela_submissoes(),
                                rx.cond(
                                    EventoState.tela_ativa == "local",
                                    tela_local(),
                                    tela_sobre(),
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            width="100%",
            max_width="1320px",
            margin="0 auto",
            padding_x="1.5rem",
            display="flex",
            align_items="center",
            justify_content="center",
            min_height="calc(100vh - 120px)",
            position="relative",
            z_index="2",
        ),

        # Rodapé Mínimo Discreto
        rx.box(
            rx.text(
                "© 2026 IV EFAC • Universidade Federal do Cariri (UFCA) • Fomento FUNCAP (Edital 03/2026) • Reflex & SQLite WAL",
                size="1",
                color=rx.color_mode_cond(light="#94a3b8", dark="var(--gray-8)"),
                text_align="center",
            ),
            padding_y="0.6rem",
            border_top=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(255, 255, 255, 0.06)"),
            background=rx.color_mode_cond(light="rgba(255, 255, 255, 0.85)", dark="rgba(6, 8, 20, 0.85)"),
            backdrop_filter="blur(10px)",
            width="100%",
            position="relative",
            z_index="2",
        ),

        min_height="100vh",
        background=rx.color_mode_cond(light="#f8fafc", dark="#060814"),
        color=rx.color_mode_cond(light="#0f172a", dark="white"),
        transition="background 0.3s ease, color 0.3s ease",
        position="relative",
        overflow="hidden",
    )
