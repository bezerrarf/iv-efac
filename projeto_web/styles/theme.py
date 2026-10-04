"""Design System & Tokens Cósmicos Profundos (UI/UX Pro Max) - IV EFAC 2026.
Pure Deep Cosmic Dark Theme com contraste WCAG AAA e regras responsivas para todas as telas.
"""

# Paleta Profunda Cósmica (WCAG AAA Contrast > 7:1)
COLOR_BG = "#060814"
COLOR_SURFACE_GLASS = "rgba(15, 23, 42, 0.72)"
COLOR_SURFACE_GLASS_HOVER = "rgba(15, 23, 42, 0.88)"
COLOR_NAVBAR_BG = "rgba(6, 8, 20, 0.88)"
COLOR_FOOTER_BG = "rgba(6, 8, 20, 0.96)"
COLOR_BORDER_SUBTLE = "rgba(255, 255, 255, 0.08)"
COLOR_BORDER_CYAN = "rgba(0, 173, 181, 0.22)"
COLOR_BORDER_CYAN_GLOW = "rgba(0, 173, 181, 0.45)"

# Tipografia
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "rgba(226, 232, 240, 0.85)"
COLOR_TEXT_MUTED = "#94A3B8"

# Acentos Cósmicos
COLOR_CYAN = "#00ADB5"
COLOR_CYAN_LIGHT = "#38BDF8"
COLOR_INDIGO = "#6366F1"
COLOR_GOLD = "#F59E0B"

# Regras de Estilo para Prevenção de Quebras Estranhas de Texto
STYLE_HEADING_RESPONSIVE = {
    "text_wrap": "balance",
    "word_break": "break-word",
}

STYLE_TEXT_RESPONSIVE = {
    "text_wrap": "pretty",
    "word_break": "break-word",
    "overflow_wrap": "anywhere",
}

STYLE_BUTTON_CHIP = {
    "white_space": "nowrap",
    "flex_shrink": "0",
}

STYLE_GLASS_CARD = {
    "background": COLOR_SURFACE_GLASS,
    "backdrop_filter": "blur(16px)",
    "border": f"1px solid {COLOR_BORDER_CYAN}",
    "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.36)",
    "border_radius": "16px",
}
