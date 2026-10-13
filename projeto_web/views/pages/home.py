"""Landing Page Única (Single Page Application) - IV EFAC 2026 (UI/UX Pro Max).
Estruturada com rolagem suave contínua, menu rápido flutuante (quick_nav),
todas as seções públicas unificadas e migração de submissões para a área autenticada.
"""

import reflex as rx
from projeto_web.views.components.navbar import navbar
from projeto_web.views.components.cosmic_background import cosmic_background
from projeto_web.views.components.quick_nav import quick_nav
from projeto_web.views.components.footer import footer
from projeto_web.styles.theme import (
    COLOR_BG,
    COLOR_NAVBAR_BG,
    COLOR_BORDER_SUBTLE,
    COLOR_TEXT_PRIMARY,
    STYLE_TEXT_RESPONSIVE,
)
from projeto_web.views.components.home_sections.tela_inicio import tela_inicio
from projeto_web.views.components.home_sections.tela_sobre import tela_sobre
from projeto_web.views.components.home_sections.tela_eixos import tela_eixos
from projeto_web.views.components.home_sections.tela_palestrantes import tela_palestrantes
from projeto_web.views.components.home_sections.tela_programacao import tela_programacao
from projeto_web.views.components.home_sections.tela_local import tela_local


def home_page() -> rx.Component:
    """Landing Page Pública do IV EFAC em fluxo contínuo de página única."""
    return rx.box(
        # Fundo Vetorial Cósmico Adaptativo
        cosmic_background(),

        # Topo com navegação integrada e alternador de tema claro/escuro
        navbar(),

        # Menu Flutuante de Rápido Acesso no Canto Inferior Direito
        quick_nav(),

        # Palco Central Contínuo de Seções (Landing Page Única)
        rx.vstack(
            # 1. Hero Section: Início & Contador
            tela_inicio(),

            # 2. Contexto Institucional: Sobre o IV EFAC
            tela_sobre(),

            # 3. Eixos Temáticos de Pesquisa
            tela_eixos(),

            # 4. Palestrantes Convidados (Keynotes) com fotos WebP e alta resolução
            tela_palestrantes(),

            # 5. Programação do Simpósio (Grade Oficial)
            tela_programacao(),

            # 6. Localização & Instituições Parceiras (Google Maps Interativo)
            tela_local(),

            spacing="6",
            width="100%",
            max_width="1320px",
            margin="0 auto",
            padding_x=rx.breakpoints(initial="1rem", sm="1.5rem", md="2rem"),
            padding_bottom="3rem",
            flex="1",
            position="relative",
            z_index="2",
        ),

        # Rodapé Oficial Integrado
        footer(),

        display="flex",
        flex_direction="column",
        min_height="100vh",
        background="transparent",
        color=COLOR_TEXT_PRIMARY,
        position="relative",
        overflow_x="hidden",
    )
