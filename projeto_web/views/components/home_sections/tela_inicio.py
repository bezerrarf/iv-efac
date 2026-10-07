import reflex as rx
from datetime import datetime
from projeto_web.state.evento_state import EventoState
from projeto_web.state.navigation_state import NavigationState
from projeto_web.controllers.evento_controller import EventoController, EixoTematico, Palestrante, Atividade
from projeto_web.styles.theme import *
from projeto_web.views.components.footer import parceiro_chip

def logo_orbital_hpc() -> rx.Component:
    """Logotipo orbital de alta tecnologia com efeito de lente gravitacional cósmica."""
    return rx.box(
        # Halo de distorção cósmica
        rx.box(
            position="absolute",
            inset="-25px",
            border_radius="50%",
            background="radial-gradient(circle, rgba(0, 173, 181, 0.35) 0%, rgba(99, 102, 241, 0.22) 50%, transparent 75%)",
            filter="blur(22px)",
            z_index="1",
        ),
        # Órbita Relativística 1 (Tracejada com brilho)
        rx.box(
            position="absolute",
            inset="6px",
            border_radius="50%",
            border="1.5px dashed rgba(0, 173, 181, 0.55)",
            transform="rotate(-28deg)",
            z_index="2",
        ),
        # Órbita Relativística 2 (Contínua)
        rx.box(
            position="absolute",
            inset="22px",
            border_radius="50%",
            border="1.5px solid rgba(129, 140, 248, 0.45)",
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
            background="#38bdf8",
            box_shadow="0 0 12px #38bdf8, 0 0 4px #ffffff",
            z_index="3",
        ),
        # Núcleo do Evento com a Logo Oficial Nova (WhatsApp Image 2026-10-03 at 15.58.16)
        rx.box(
            rx.image(
                src="/logo_ivefac.jpeg",
                alt="Logo Oficial IV EFAC 2026",
                width="135px",
                height="135px",
                border_radius="50%",
                object_fit="cover",
            ),
            width="135px",
            height="135px",
            border_radius="50%",
            border="3px solid rgba(0, 173, 181, 0.85)",
            box_shadow="0 0 35px rgba(0, 173, 181, 0.55), inset 0 0 20px rgba(16, 52, 96, 0.6)",
            display="grid",
            place_items="center",
            position="relative",
            z_index="4",
            overflow="hidden",
        ),
        width="200px",
        height="200px",
        display="grid",
        place_items="center",
        position="relative",
        margin="0 auto",
    )


def display_hud_contagem() -> rx.Component:
    """Display digital estilo relógio atômico para o início do simpósio (11/11 às 08h00)
    com transição para mensagens de boas-vindas e citações inspiradoras de cientistas.
    """
    alvo = datetime(2026, 11, 11, 8, 0, 0)
    agora = datetime.now()
    diff_segundos = max(int((alvo - agora).total_seconds()), 0)
    init_dias = diff_segundos // 86400
    init_horas = (diff_segundos % 86400) // 3600
    init_min = (diff_segundos % 3600) // 60
    init_seg = diff_segundos % 60

    def hud_item(id_elem: str, val_inicial: str, label: str) -> rx.Component:
        return rx.box(
            rx.vstack(
                rx.heading(
                    val_inicial,
                    id=id_elem,
                    size="5",
                    weight="bold",
                    color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                ),
                rx.text(
                    label,
                    size="1",
                    color=rx.color_mode_cond(light="#64748b", dark="var(--gray-9)"),
                    text_transform="uppercase",
                    letter_spacing="1px",
                ),
                spacing="0",
                align="center",
            ),
            background=rx.color_mode_cond(light="rgba(255, 255, 255, 0.9)", dark="rgba(15, 23, 42, 0.8)"),
            border=rx.color_mode_cond(light="1px solid #e2e8f0", dark="1px solid rgba(0, 173, 181, 0.3)"),
            border_radius="10px",
            padding="0.5rem 0.9rem",
            min_width="68px",
            box_shadow="0 4px 12px rgba(0, 0, 0, 0.15)",
        )

    # 1. Visão de Contagem Regressiva Ativa
    visao_relogio = rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="8px",
                    height="8px",
                    border_radius="50%",
                    background="#00ADB5",
                    box_shadow="0 0 10px #00ADB5",
                ),
                rx.text(
                    "CONTAGEM REGRESSIVA PARA ABERTURA",
                    size="1",
                    weight="bold",
                    letter_spacing="1.5px",
                    color=rx.color_mode_cond(light="#103460", dark="#00ADB5"),
                ),
                rx.badge("11/11 às 08h00", color_scheme="cyan", variant="surface", size="1"),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                hud_item("hud-dias", str(init_dias).zfill(2), "Dias"),
                hud_item("hud-horas", str(init_horas).zfill(2), "Horas"),
                hud_item("hud-min", str(init_min).zfill(2), "Min"),
                hud_item("hud-seg", str(init_seg).zfill(2), "Seg"),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                rx.button(
                    rx.hstack(
                        rx.icon(tag="sparkles", size=14, color="#38bdf8"),
                        rx.text("Ver Mensagens Inspiradoras dos Cientistas", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    size="1",
                    variant="ghost",
                    color_scheme="cyan",
                    cursor="pointer",
                    on_click=EventoState.alternar_preview_evento_iniciado,
                    padding="0.2rem 0.5rem",
                ),
                spacing="1",
                align="center",
                margin_top="0.3rem",
            ),
            spacing="2",
            align="start",
        ),
        id="hud-countdown-container",
    )

    # 2. Visão de Evento em Andamento / Mensagens Inspiradoras dos Cientistas
    visao_evento_iniciado = rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    width="10px",
                    height="10px",
                    border_radius="50%",
                    background="#22c55e",
                    box_shadow="0 0 12px #22c55e",
                ),
                rx.badge("AO VIVO • SIMPÓSIO EM ANDAMENTO", color_scheme="green", variant="surface", size="2"),
                rx.spacer(),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="clock", size=13),
                        rx.text("Ver Relógio", size="1"),
                        spacing="1",
                        align="center",
                    ),
                    size="1",
                    variant="ghost",
                    color_scheme="gray",
                    cursor="pointer",
                    on_click=EventoState.alternar_preview_evento_iniciado,
                ),
                spacing="2",
                align="center",
                width="100%",
            ),
            rx.heading(
                "Aproveite Cada Momento do IV EFAC 2026!",
                size="4",
                weight="bold",
                color="white",
            ),
            rx.text(
                "Abertura oficial realizada às 08h00! Participe ativamente das conferências magnas, apresentações orais e minicursos no Campus Brejo Santo – UFCA.",
                size="2",
                color="var(--gray-10)",
                line_height="1.5",
            ),
            # Card com Mensagem Inspiradora do Cientista (Carrossel Automático com intervalo de 10s)
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag=EventoState.frase_cientista_icone, size=22, color=EventoState.frase_cientista_cor),
                        rx.vstack(
                            rx.text(EventoState.frase_cientista_autor, size="2", weight="bold", color="white"),
                            rx.text(EventoState.frase_cientista_area, size="1", color=EventoState.frase_cientista_cor),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.badge("Inspiração Científica", color_scheme="cyan", variant="soft", size="1"),
                        align="center",
                        width="100%",
                    ),
                    rx.text(
                        EventoState.frase_cientista_texto,
                        size="2",
                        color="var(--gray-11)",
                        font_style="italic",
                        line_height="1.6",
                    ),
                    # Controles de navegação de citações
                    rx.hstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="chevron-left", size=14),
                                rx.text("Anterior", size="1"),
                                spacing="1",
                                align="center",
                            ),
                            size="1",
                            variant="outline",
                            color_scheme="gray",
                            on_click=EventoState.frase_anterior_cientista,
                        ),
                        rx.text(
                            EventoState.frase_cientista_paginacao,
                            size="1",
                            color="var(--gray-9)",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.text("Próxima", size="1"),
                                rx.icon(tag="chevron-right", size=14),
                                spacing="1",
                                align="center",
                            ),
                            id="btn-proxima-frase-cientista",
                            size="1",
                            variant="outline",
                            color_scheme="cyan",
                            on_click=EventoState.proxima_frase_cientista,
                        ),
                        spacing="3",
                        align="center",
                        justify="between",
                        width="100%",
                        padding_top="0.4rem",
                    ),
                    spacing="2",
                    align="start",
                    width="100%",
                ),
                padding=rx.breakpoints(initial="0.75rem 0.9rem", sm="1rem 1.25rem"),
                border_radius="14px",
                background="rgba(15, 23, 42, 0.8)",
                border="1px solid rgba(0, 173, 181, 0.25)",
                box_shadow="0 6px 20px rgba(0, 0, 0, 0.25)",
                width="100%",
                max_width="580px",
            ),
            # Script de transição automática do carrossel a cada 10 segundos
            rx.script("""
                if (!window._cientistas_carousel_active) {
                    window._cientistas_carousel_active = true;
                    setInterval(function() {
                        var btn = document.getElementById("btn-proxima-frase-cientista");
                        if (btn) {
                            btn.click();
                        }
                    }, 10000);
                }
            """),
            spacing="2",
            align="start",
        ),
        id="hud-live-container",
    )

    # Script JavaScript nativo para atualização contínua a cada segundo
    script_countdown = rx.script("""
    (function() {
        function tickCountdown() {
            var alvo = new Date("2026-11-11T08:00:00-03:00").getTime();
            var agora = new Date().getTime();
            var diff = alvo - agora;

            var elDias = document.getElementById("hud-dias");
            var elHoras = document.getElementById("hud-horas");
            var elMin = document.getElementById("hud-min");
            var elSeg = document.getElementById("hud-seg");

            if (diff > 0) {
                var dias = Math.floor(diff / (1000 * 60 * 60 * 24));
                var horas = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                var min = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                var seg = Math.floor((diff % (1000 * 60)) / 1000);

                if (elDias) elDias.innerText = String(dias).padStart(2, '0');
                if (elHoras) elHoras.innerText = String(horas).padStart(2, '0');
                if (elMin) elMin.innerText = String(min).padStart(2, '0');
                if (elSeg) elSeg.innerText = String(seg).padStart(2, '0');
            }
        }
        setInterval(tickCountdown, 1000);
        tickCountdown();
    })();
    """)

    return rx.box(
        rx.cond(
            EventoState.evento_iniciado_preview,
            visao_evento_iniciado,
            visao_relogio,
        ),
        script_countdown,
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
                    style=STYLE_BUTTON_CHIP,
                ),
                rx.heading(
                    "IV Encontro de Física e Astronomia do Cariri",
                    size=rx.breakpoints(initial="6", sm="7", md="8", lg="9"),
                    weight="bold",
                    color="white",
                    line_height="1.15",
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(
                    "Fronteiras da Física Contemporânea, Formação Científica e Integração Regional",
                    size=rx.breakpoints(initial="3", sm="4"),
                    weight="medium",
                    color=COLOR_CYAN_LIGHT,
                    style=STYLE_HEADING_RESPONSIVE,
                ),
                rx.text(
                    "Convergência de Astrofísica Relativística, Relatividade Geral, "
                    "Computação de Alto Desempenho (HPC) e Ensino de Ciências no interior do Ceará.",
                    size=rx.breakpoints(initial="2", sm="3"),
                    color="var(--gray-10)",
                    line_height="1.6",
                    max_width="640px",
                    style=STYLE_TEXT_RESPONSIVE,
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
                            background="linear-gradient(135deg, #00ADB5 0%, #103460 100%)",
                            color="white",
                            box_shadow="0 4px 18px rgba(0, 173, 181, 0.4)",
                            _hover={"transform": "translateY(-1px)", "box_shadow": "0 6px 24px rgba(0, 173, 181, 0.55)"},
                            transition="all 0.2s ease",
                            style=STYLE_BUTTON_CHIP,
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
                        border="1.5px solid #00ADB5",
                        color=COLOR_CYAN,
                        _hover={"background": "rgba(0, 173, 181, 0.15)"},
                        on_click=NavigationState.set_tela("submissoes"),
                        style=STYLE_BUTTON_CHIP,
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
                                rx.heading(s["valor"], size="6", weight="bold", color=COLOR_CYAN),
                                rx.text(s["rotulo"], size="1", color="var(--gray-10)", text_align="center", style=STYLE_TEXT_RESPONSIVE),
                                spacing="0",
                                align="center",
                            ),
                            background=COLOR_SURFACE_GLASS,
                            backdrop_filter="blur(12px)",
                            border=f"1px solid {COLOR_BORDER_CYAN}",
                            border_radius="14px",
                            padding="0.8rem 1rem",
                            text_align="center",
                            box_shadow="0 4px 18px rgba(0, 0, 0, 0.3)",
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
            padding_y=rx.breakpoints(initial="1.5rem", md="2rem"),
        ),
        width="100%",
    )


# --- 2. TELA SOBRE: HISTÓRICO BINGO & FOMENTO ---

