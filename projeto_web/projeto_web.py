"""Ponto de entrada principal da aplicação Reflex IV EFAC 2026 (MVC).
Encontro de Física e Astronomia do Cariri • UFCA / IFE.
"""

import reflex as rx
from projeto_web.views.pages.home import home_page
from projeto_web.views.pages.cronograma import cronograma_page
from projeto_web.views.pages.inscricao import inscricao_page

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap",
    ],
    style={
        "font_family": "'Plus Jakarta Sans', sans-serif",
    },
    head_components=[
        rx.html('<link rel="icon" type="image/x-icon" href="/favicon.ico"/>'),
        rx.html('<link rel="icon" type="image/png" href="/favicon.png"/>'),
        rx.html('<link rel="apple-touch-icon" href="/favicon.png"/>'),
        rx.html('<style>a[href*="reflex.dev"] { display: none !important; opacity: 0 !important; pointer-events: none !important; visibility: hidden !important; }</style>'),
    ],
)

# Registro das Rotas do Sistema com SEO e OpenGraph
app.add_page(
    home_page,
    route="/",
    title="IV EFAC • Encontro de Física e Astronomia do Cariri (UFCA)",
    description="IV Encontro de Física e Astronomia do Cariri. Fronteiras da Física Contemporânea, Formação Científica e Integração Regional. 11 e 12 de Novembro de 2026.",
    meta=[
        {"property": "og:title", "content": "IV EFAC 2026 • Encontro de Física e Astronomia do Cariri"},
        {"property": "og:description", "content": "Fronteiras da Física Contemporânea, Formação Científica e Integração Regional • UFCA Campus Brejo Santo"},
        {"property": "og:type", "content": "website"},
        {"name": "keywords", "content": "Física, Astronomia, UFCA, Cariri, FUNCAP, Astrofísica, Brejo Santo, Ceará"},
    ],
)

app.add_page(
    cronograma_page,
    route="/cronograma",
    title="Programação Oficial • IV EFAC 2026",
    description="Grade horária oficial de 2 dias do IV EFAC (11 e 12/11/2026): Conferências Magnas, Minicurso Python, Mesas-Redondas e Sessões Orais.",
)

app.add_page(
    inscricao_page,
    route="/inscricao",
    title="Inscrição & Credencial Oficial • IV EFAC 2026",
    description="Portal oficial de credenciamento do IV EFAC no Campus Brejo Santo – UFCA com emissão de certificado oficial.",
)

app.add_page(
    inscricao_page,
    route="/login",
    title="Login & Acesso • IV EFAC 2026",
    description="Acesso ao portal de inscritos e painel administrativo do IV EFAC 2026.",
)
