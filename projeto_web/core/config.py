"""Configurações globais e caminhos de dados do AstroData 2026."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_FILE = BASE_DIR / "evento.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_FILE}")
CAPACIDADE_MAXIMA_EVENTO = 300
