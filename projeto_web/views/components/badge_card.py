"""Componente de Cartão de Identificação / Crachá Digital Oficial do IV EFAC (View).
Baseado fielmente na identidade visual oficial 'WhatsApp Image 2026-10-03 at 16.05.42'.
Permite inserção de foto personalizada, alternância entre Participante e Palestrante,
e suporte a impressão e download direto do crachá.
"""

import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.styles.theme import (
    COLOR_CYAN,
    COLOR_CYAN_LIGHT,
    COLOR_BORDER_CYAN,
    COLOR_SURFACE_GLASS,
    STYLE_BUTTON_CHIP,
    STYLE_HEADING_RESPONSIVE,
    STYLE_TEXT_RESPONSIVE,
)


AVATAR_PRESETS = [
    {
        "nome": "Soldadinho do Araripe",
        "url": "/logo_ivefac.jpeg",
        "icone": "feather",
    },
    {
        "nome": "Cosmo Cariri",
        "url": "/fundo_cosmico.jpeg",
        "icone": "orbit",
    },
    {
        "nome": "Banner IV EFAC",
        "url": "/cariri_cosmico_banner.jpeg",
        "icone": "sparkles",
    },
    {
        "nome": "Poster Oficial",
        "url": "/poster_oficial_ivefac.jpeg",
        "icone": "award",
    },
]


def badge_photo_element() -> rx.Component:
    """Círculo de foto do participante/palestrante com moldura orbital cósmica e glow ciano."""
    tem_foto = EventoState.user_foto_url != ""

    return rx.box(
        # Halo de brilho orbital
        rx.box(
            position="absolute",
            inset="-10px",
            border_radius="50%",
            background="radial-gradient(circle, rgba(0, 173, 181, 0.4) 0%, rgba(99, 102, 241, 0.2) 60%, transparent 75%)",
            filter="blur(10px)",
            z_index="1",
        ),
        # Anel Orbital Ciano Neon
        rx.box(
            position="absolute",
            inset="-4px",
            border_radius="50%",
            border="2px solid rgba(0, 173, 181, 0.8)",
            box_shadow="0 0 16px rgba(0, 173, 181, 0.6), inset 0 0 8px rgba(0, 173, 181, 0.3)",
            z_index="2",
        ),
        # Foto ou Ícone Placeholder
        rx.cond(
            tem_foto,
            rx.image(
                src=EventoState.user_foto_url,
                alt=EventoState.user_nome,
                width="140px",
                height="140px",
                border_radius="50%",
                object_fit="cover",
                position="relative",
                z_index="3",
            ),
            rx.box(
                rx.vstack(
                    rx.icon(tag="camera", size=32, color=COLOR_CYAN_LIGHT),
                    rx.text("Foto do(a)", size="1", weight="bold", color="white"),
                    rx.text(
                        rx.cond(EventoState.badge_modo == "palestrante", "palestrante", "participante"),
                        size="1",
                        color="var(--gray-9)",
                    ),
                    spacing="0",
                    align="center",
                ),
                width="140px",
                height="140px",
                border_radius="50%",
                background="linear-gradient(145deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.8))",
                border="2px dashed rgba(0, 173, 181, 0.5)",
                display="grid",
                place_items="center",
                position="relative",
                z_index="3",
                cursor="pointer",
            ),
        ),
        position="relative",
        width="140px",
        height="140px",
        display="grid",
        place_items="center",
    )


def cartao_identificacao_digital() -> rx.Component:
    """Card de Identificação / Crachá Digital fiel ao template 'WhatsApp Image 2026-10-03 at 16.05.42'."""
    is_palestrante = EventoState.badge_modo == "palestrante"

    return rx.box(
        # Contêiner Principal do Crachá com Estilo de Pôster Cósmico
        rx.box(
            rx.vstack(
                # Topo: Cabeçalho Institucional UFCA / IFE
                rx.vstack(
                    rx.text(
                        "UNIVERSIDADE FEDERAL DO CARIRI – UFCA",
                        size="1",
                        weight="bold",
                        letter_spacing="0.12em",
                        color="rgba(255, 255, 255, 0.9)",
                        text_align="center",
                    ),
                    rx.text(
                        "Instituto de Formação de Educadores – IFE",
                        size="1",
                        color="var(--gray-9)",
                        letter_spacing="0.08em",
                        text_align="center",
                    ),
                    spacing="0",
                    align="center",
                    width="100%",
                ),
                # Logotipo Oficial IV EFAC & Subtítulo
                rx.hstack(
                    rx.image(
                        src="/logo_ivefac.jpeg",
                        alt="Logo IV EFAC 2026",
                        width="48px",
                        height="48px",
                        border_radius="50%",
                        object_fit="cover",
                        border="1.5px solid #00ADB5",
                        box_shadow="0 0 12px rgba(0, 173, 181, 0.6)",
                    ),
                    rx.vstack(
                        rx.hstack(
                            rx.heading("IV EFAC", size="5", weight="bold", color="white", letter_spacing="1px"),
                            rx.badge("2026", color_scheme="cyan", variant="solid", size="1"),
                            spacing="1",
                            align="center",
                        ),
                        rx.text(
                            "Encontro de Física e Astronomia do Cariri",
                            size="1",
                            color="rgba(226, 232, 240, 0.8)",
                            weight="medium",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                    width="100%",
                    padding_y="0.35rem",
                    border_bottom="1px solid rgba(255, 255, 255, 0.1)",
                ),
                # Corpo Central: Foto Circular + Dados do Inscrito/Palestrante
                rx.hstack(
                    # Coluna Esquerda: Moldura de Foto Orbital
                    badge_photo_element(),
                    # Coluna Direita: Informações
                    rx.vstack(
                        # Pill Tag da Categoria
                        rx.cond(
                            is_palestrante,
                            rx.badge(
                                rx.hstack(
                                    rx.icon(tag="mic", size=12),
                                    rx.text("PALESTRA CONVIDADA", size="1", weight="bold"),
                                    spacing="1",
                                    align="center",
                                ),
                                color_scheme="red",
                                variant="solid",
                                radius="full",
                                padding_x="0.6rem",
                                padding_y="0.2rem",
                            ),
                            rx.cond(
                                EventoState.is_admin,
                                rx.badge(
                                    rx.hstack(
                                        rx.icon(tag="shield", size=12),
                                        rx.text("COORDENAÇÃO / ADMIN", size="1", weight="bold"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    color_scheme="amber",
                                    variant="solid",
                                    radius="full",
                                    padding_x="0.6rem",
                                    padding_y="0.2rem",
                                ),
                                rx.cond(
                                    EventoState.is_supervisor,
                                    rx.badge(
                                        rx.hstack(
                                            rx.icon(tag="clipboard-check", size=12),
                                            rx.text("SUPERVISOR(A) OFICIAL", size="1", weight="bold"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        color_scheme="violet",
                                        variant="solid",
                                        radius="full",
                                        padding_x="0.6rem",
                                        padding_y="0.2rem",
                                    ),
                                    rx.badge(
                                        rx.hstack(
                                            rx.icon(tag="user", size=12),
                                            rx.text("PARTICIPANTE OFICIAL", size="1", weight="bold"),
                                            spacing="1",
                                            align="center",
                                        ),
                                        color_scheme="cyan",
                                        variant="solid",
                                        radius="full",
                                        padding_x="0.6rem",
                                        padding_y="0.2rem",
                                    ),
                                ),
                            ),
                        ),
                        # Nome
                        rx.heading(
                            rx.cond(
                                is_palestrante,
                                EventoState.badge_palestrante_nome,
                                rx.cond(EventoState.user_nome != "", EventoState.user_nome, "Nome do Participante"),
                            ),
                            size="5",
                            weight="bold",
                            color="white",
                            line_height="1.2",
                        ),
                        # Instituição
                        rx.text(
                            rx.cond(
                                is_palestrante,
                                EventoState.badge_palestrante_inst,
                                rx.cond(EventoState.user_instituicao != "", EventoState.user_instituicao, "Universidade / Polo"),
                            ),
                            size="2",
                            color="var(--gray-9)",
                        ),
                        # Linha Divisória Vermelha / Rubro Cariri
                        rx.box(
                            width="60px",
                            height="2.5px",
                            background="linear-gradient(90deg, #ef4444 0%, #dc2626 100%)",
                            border_radius="2px",
                            margin_y="0.25rem",
                        ),
                        # Tema / Eixo / Modalidade
                        rx.text(
                            rx.cond(
                                is_palestrante,
                                EventoState.badge_palestrante_tema,
                                EventoState.user_area,
                            ),
                            size="2",
                            weight="bold",
                            color=COLOR_CYAN,
                        ),
                        # Código de Check-in em Destaque
                        rx.cond(
                            EventoState.badge_modo == "participante",
                            rx.hstack(
                                rx.text("Check-in:", size="1", color="var(--gray-9)"),
                                rx.badge(
                                    rx.cond(EventoState.user_codigo != "", EventoState.user_codigo, "ASTRO-XXXXXX"),
                                    color_scheme="cyan",
                                    variant="soft",
                                    size="1",
                                ),
                                rx.badge(
                                    rx.cond(EventoState.user_modalidade != "", EventoState.user_modalidade, "Presencial"),
                                    color_scheme="indigo",
                                    variant="surface",
                                    size="1",
                                ),
                                spacing="1",
                                align="center",
                            ),
                            rx.text(
                                "Conferência e discussão acadêmica das fronteiras da Física Contemporânea.",
                                size="1",
                                color="var(--gray-10)",
                            ),
                        ),
                        align="start",
                        spacing="1",
                        flex="1",
                    ),
                    spacing="4",
                    align="center",
                    width="100%",
                    padding_y="0.75rem",
                ),
                # Barra Inferior com Ícones: Data, Horário e Local
                rx.box(
                    rx.grid(
                        # Data
                        rx.hstack(
                            rx.icon(tag="calendar", size=18, color="#ef4444"),
                            rx.vstack(
                                rx.text("11 e 12 nov 2026", size="1", weight="bold", color="white"),
                                rx.text("Quarta e Quinta", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        # Horário
                        rx.hstack(
                            rx.icon(tag="clock", size=18, color="#f59e0b"),
                            rx.vstack(
                                rx.text(
                                    rx.cond(is_palestrante, EventoState.badge_palestrante_horario, "08h00"),
                                    size="1",
                                    weight="bold",
                                    color="white",
                                ),
                                rx.text("Abertura Oficial", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        # Local
                        rx.hstack(
                            rx.icon(tag="map-pin", size=18, color="#ef4444"),
                            rx.vstack(
                                rx.text("UFCA • Brejo Santo", size="1", weight="bold", color="white"),
                                rx.text("Ceará • Presencial", size="1", color="var(--gray-9)"),
                                spacing="0",
                                align="start",
                            ),
                            spacing="2",
                            align="center",
                        ),
                        columns=rx.breakpoints(initial="1", sm="3"),
                        spacing="2",
                        width="100%",
                        align="center",
                    ),
                    background="rgba(10, 15, 30, 0.8)",
                    border="1px solid rgba(0, 173, 181, 0.25)",
                    border_radius="12px",
                    padding="0.75rem 1rem",
                    width="100%",
                    box_shadow="inset 0 0 15px rgba(0, 0, 0, 0.4)",
                ),
                # Rodapé de Chancela e Apoio
                rx.hstack(
                    rx.badge("Fomento FUNCAP", color_scheme="cyan", variant="soft", size="1"),
                    rx.spacer(),
                    rx.text("Documento Oficial de Identificação Acadêmica", size="1", color="var(--gray-9)"),
                    align="center",
                    width="100%",
                    padding_top="0.25rem",
                ),
                spacing="3",
                width="100%",
            ),
            # Background Cósmico Fiel à Imagem
            background="linear-gradient(165deg, rgba(8, 12, 28, 0.96) 0%, rgba(16, 28, 54, 0.94) 55%, rgba(6, 9, 20, 0.98) 100%)",
            border="1.5px solid rgba(0, 173, 181, 0.45)",
            box_shadow="0 14px 50px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 173, 181, 0.25)",
            border_radius="20px",
            padding="1.5rem",
            width="100%",
            max_width="620px",
            position="relative",
            overflow="hidden",
        ),
        # Painel de Customização e Ações do Crachá (Upload, Presets e Download)
        rx.vstack(
            rx.hstack(
                # Alternador de Modo (Participante / Palestrante)
                rx.button(
                    rx.hstack(
                        rx.icon(tag="user", size=14),
                        rx.text("Visualizar como Participante", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    variant=rx.cond(EventoState.badge_modo == "participante", "solid", "outline"),
                    color_scheme="cyan",
                    size="2",
                    on_click=EventoState.set_badge_modo("participante"),
                    style=STYLE_BUTTON_CHIP,
                ),
                rx.button(
                    rx.hstack(
                        rx.icon(tag="mic", size=14),
                        rx.text("Modelo Palestrante", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    variant=rx.cond(EventoState.badge_modo == "palestrante", "solid", "outline"),
                    color_scheme="indigo",
                    size="2",
                    on_click=EventoState.set_badge_modo("palestrante"),
                    style=STYLE_BUTTON_CHIP,
                ),
                # Botão de Impressão / Salvar PDF
                rx.button(
                    rx.hstack(
                        rx.icon(tag="printer", size=14),
                        rx.text("Imprimir / Salvar Crachá", size="2"),
                        spacing="1",
                        align="center",
                    ),
                    variant="outline",
                    color_scheme="green",
                    size="2",
                    on_click=rx.call_script("window.print()"),
                    style=STYLE_BUTTON_CHIP,
                ),
                spacing="2",
                wrap="wrap",
                justify="center",
                width="100%",
            ),
            # Inserção de Foto / Upload de Celular / PC / Link da Internet / Presets
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.icon(tag="image", size=18, color=COLOR_CYAN),
                        rx.heading("Foto da Carteirinha Digital do Participante", size="3", weight="bold", color="white"),
                        align="center",
                        spacing="2",
                    ),
                    rx.text(
                        "Escolha uma foto sua enviada do computador, celular ou dispositivo móvel, ou cole um link da internet.",
                        size="1",
                        color="var(--gray-10)",
                    ),
                    rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="smartphone", size=13),
                                    rx.text("Do Computador ou Celular", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="upload",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="link", size=13),
                                    rx.text("Link da Internet (URL)", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="link",
                            ),
                            rx.tabs.trigger(
                                rx.hstack(
                                    rx.icon(tag="sparkles", size=13),
                                    rx.text("Avatares Temáticos", size="1"),
                                    spacing="1",
                                    align="center",
                                ),
                                value="presets",
                            ),
                            size="1",
                        ),
                        rx.tabs.content(
                            # Upload do PC ou Celular
                            rx.vstack(
                                rx.upload(
                                    rx.vstack(
                                        rx.icon(tag="upload-cloud", size=24, color=COLOR_CYAN),
                                        rx.text("Clique para escolher uma imagem do seu Computador ou Celular", size="2", weight="bold", color="white"),
                                        rx.text("Suporta fotos da galeria, câmera do celular ou arquivos (JPG, PNG, WEBP)", size="1", color="var(--gray-9)"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    id="upload_foto_carteirinha",
                                    accept={"image/*": [".jpg", ".jpeg", ".png", ".webp"]},
                                    max_files=1,
                                    border="1.5px dashed rgba(0, 173, 181, 0.4)",
                                    padding="1.25rem",
                                    border_radius="10px",
                                    background="rgba(15, 23, 42, 0.5)",
                                    _hover={"border_color": COLOR_CYAN, "background": "rgba(0, 173, 181, 0.08)"},
                                    cursor="pointer",
                                    width="100%",
                                ),
                                rx.button(
                                    rx.hstack(
                                        rx.icon(tag="check", size=14),
                                        rx.text("Confirmar e Salvar Foto no Cartão", size="1"),
                                        spacing="1",
                                        align="center",
                                    ),
                                    size="2",
                                    color_scheme="cyan",
                                    on_click=EventoState.handle_upload_foto(rx.upload_files(upload_id="upload_foto_carteirinha")),
                                    style=STYLE_BUTTON_CHIP,
                                ),
                                spacing="2",
                                align="center",
                                width="100%",
                                padding_top="0.5rem",
                            ),
                            value="upload",
                        ),
                        rx.tabs.content(
                            # Link da Internet
                            rx.vstack(
                                rx.text("Cole o endereço ou URL direta da sua foto na internet:", size="1", color="var(--gray-10)"),
                                rx.hstack(
                                    rx.input(
                                        placeholder="Ex: https://meusite.com/minha_foto.jpg",
                                        value=EventoState.badge_foto_input,
                                        on_change=EventoState.set_badge_foto_input,
                                        size="2",
                                        flex="1",
                                    ),
                                    rx.button(
                                        "Aplicar Link",
                                        size="2",
                                        color_scheme="cyan",
                                        on_click=EventoState.salvar_foto_perfil,
                                        style=STYLE_BUTTON_CHIP,
                                    ),
                                    spacing="2",
                                    width="100%",
                                ),
                                spacing="2",
                                width="100%",
                                padding_top="0.5rem",
                            ),
                            value="link",
                        ),
                        rx.tabs.content(
                            # Presets Temáticos
                            rx.vstack(
                                rx.text("Selecione um dos avatares temáticos oficiais do simpósio:", size="1", color="var(--gray-10)"),
                                rx.hstack(
                                    *[
                                        rx.tooltip(
                                            rx.button(
                                                rx.hstack(
                                                    rx.icon(tag=preset["icone"], size=12),
                                                    rx.text(preset["nome"], size="1"),
                                                    spacing="1",
                                                    align="center",
                                                ),
                                                size="1",
                                                variant="surface",
                                                color_scheme="cyan",
                                                on_click=EventoState.definir_avatar_preset(preset["url"]),
                                                style=STYLE_BUTTON_CHIP,
                                            ),
                                            content=f"Usar avatar {preset['nome']}",
                                        )
                                        for preset in AVATAR_PRESETS
                                    ],
                                    spacing="2",
                                    wrap="wrap",
                                    align="center",
                                ),
                                spacing="2",
                                width="100%",
                                padding_top="0.5rem",
                            ),
                            value="presets",
                        ),
                        default_value="upload",
                        width="100%",
                    ),
                    spacing="3",
                    width="100%",
                ),
                background="rgba(15, 23, 42, 0.7)",
                border="1px solid rgba(255, 255, 255, 0.08)",
                border_radius="12px",
                padding="1.25rem",
                width="100%",
                max_width="620px",
            ),
            spacing="3",
            width="100%",
            align="center",
            margin_top="1rem",
        ),
        width="100%",
        display="flex",
        flex_direction="column",
        align_items="center",
    )
