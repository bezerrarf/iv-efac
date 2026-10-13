"""Sistema de Design e Identidade Visual Cósmica Unificada (IV EFAC 2026).
Paleta Oficial Cósmica Exclusiva (Dark Cyber-Astrofísica de Alto Contraste AAA).
Tema claro totalmente removido conforme diretriz do evento.
"""

import reflex as rx

# --- PALETA CROMÁTICA PRINCIPAL (CÓSMICA PURA) ---
COLOR_PRIMARY_DEEP = "#060814"
COLOR_BG = "#060814"
COLOR_BG_GRADIENT = "radial-gradient(circle at 50% 15%, rgba(16, 52, 96, 0.45) 0%, #060814 85%)"
COLOR_SURFACE_GLASS = "rgba(11, 19, 43, 0.72)"
COLOR_SURFACE_GLASS_HOVER = "rgba(16, 52, 96, 0.50)"
COLOR_NAVBAR_BG = "rgba(6, 8, 20, 0.88)"
COLOR_FOOTER_BG = "rgba(6, 8, 20, 0.96)"

# Acentos Cósmicos
COLOR_CYAN = "#00ADB5"
COLOR_CYAN_LIGHT = "#38BDF8"
COLOR_CYAN_GLOW = "0 0 24px rgba(0, 173, 181, 0.5)"
COLOR_INDIGO = "#6366F1"
COLOR_INDIGO_ACCENT = "#6366F1"
COLOR_PURPLE_ACCENT = "#A855F7"
COLOR_GOLD = "#F59E0B"
COLOR_BORDER_CYAN = "rgba(0, 173, 181, 0.35)"
COLOR_BORDER_CYAN_GLOW = "rgba(0, 173, 181, 0.6)"
COLOR_BORDER_SUBTLE = "rgba(255, 255, 255, 0.12)"

# Tipografia Luminosa e Cinzas Claros de Alto Contraste AAA (Cinza escuro removido)
COLOR_TEXT_PRIMARY = "#FFFFFF"
COLOR_TEXT_SECONDARY = "#E2E8F0"
COLOR_TEXT_MUTED = "#CBD5E1"
COLOR_TEXT_FAINT = "#94A3B8"

# Estilos Utilitários
STYLE_GLASS_CARD = {
    "background": COLOR_SURFACE_GLASS,
    "backdrop_filter": "blur(16px)",
    "border": f"1px solid {COLOR_BORDER_CYAN}",
    "box_shadow": "0 8px 32px rgba(0, 0, 0, 0.4)",
}

STYLE_BUTTON_CHIP = {
    "font_size": "clamp(0.72rem, 1.2vw, 0.88rem)",
    "white_space": "nowrap",
}

STYLE_HEADING_RESPONSIVE = {
    "word_break": "break-word",
    "overflow_wrap": "break-word",
    "text_wrap": "balance",
    "hyphens": "auto",
}

STYLE_TEXT_RESPONSIVE = {
    "word_break": "break-word",
    "overflow_wrap": "break-word",
    "text_wrap": "pretty",
    "font_size": "clamp(0.75rem, 1.3vw, 0.95rem)",
    "color": COLOR_TEXT_MUTED,
}
