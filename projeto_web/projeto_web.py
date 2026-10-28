"""Ponto de entrada principal da aplicação Reflex IV EFAC 2026 (MVC).
Encontro de Física e Astronomia do Cariri • UFCA / IFE.
"""

import reflex as rx
from projeto_web.views.pages.home import home_page
from projeto_web.views.pages.cronograma import cronograma_page
from projeto_web.views.pages.inscricao import inscricao_page
from projeto_web.views.pages.normas_submissao import normas_submissao_page
from projeto_web.state.evento_state import EventoState

app = rx.App(
    stylesheets=[
        "https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap",
        "/styles.css",
    ],
    style={
        "font_family": "'Plus Jakarta Sans', sans-serif",
    },
    head_components=[
        rx.el.link(rel="icon", type="image/x-icon", href="/favicon.ico"),
        rx.el.link(rel="icon", type="image/png", href="/favicon.png"),
        rx.el.link(rel="apple-touch-icon", href="/favicon.png"),
        rx.el.link(rel="canonical", href="https://ivefac.com.br/"),
        # Diretrizes Oficiais para Motores de Busca (Googlebot, Bingbot)
        rx.el.meta(name="robots", content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"),
        rx.el.meta(name="googlebot", content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1"),
        rx.el.meta(name="author", content="Universidade Federal do Cariri (UFCA) / IFE"),
        rx.el.meta(name="language", content="pt-BR"),
        rx.el.meta(name="geo.region", content="BR-CE"),
        rx.el.meta(name="geo.placename", content="Brejo Santo"),
        # OpenGraph / Redes Sociais Globais
        rx.el.meta(property="og:site_name", content="IV EFAC 2026 • UFCA"),
        rx.el.meta(property="og:locale", content="pt_BR"),
        rx.el.meta(property="og:url", content="https://ivefac.com.br/"),
        rx.el.meta(property="og:image", content="https://ivefac.com.br/poster_oficial_ivefac.jpeg"),
        rx.el.meta(property="og:image:alt", content="Poster Oficial do IV Encontro de Física e Astronomia do Cariri (UFCA)"),
        rx.el.meta(name="twitter:card", content="summary_large_image"),
        rx.el.meta(name="twitter:image", content="https://ivefac.com.br/poster_oficial_ivefac.jpeg"),
        # Schema.org Structured Data (JSON-LD) para Evento Acadêmico no Google
        rx.el.script(
            '{"@context": "https://schema.org", "@type": "EducationEvent", "name": "IV EFAC - Encontro de Física e Astronomia do Cariri", "alternateName": "IV EFAC 2026 • UFCA", "description": "Fronteiras da Física Contemporânea, Formação Científica e Integração Regional. Encontro acadêmico sediado no Instituto de Formação de Educadores (IFE) - UFCA Campus Brejo Santo com apoio da FUNCAP.", "startDate": "2026-11-11T08:00:00-03:00", "endDate": "2026-11-12T18:00:00-03:00", "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode", "location": {"@type": "Place", "name": "Universidade Federal do Cariri (UFCA) - Campus Brejo Santo (IFE)", "address": {"@type": "PostalAddress", "addressLocality": "Brejo Santo", "addressRegion": "CE", "addressCountry": "BR"}}, "image": "https://ivefac.com.br/poster_oficial_ivefac.jpeg", "organizer": {"@type": "EducationalOrganization", "name": "Universidade Federal do Cariri (UFCA)", "url": "https://ufca.edu.br"}, "sponsor": {"@type": "Organization", "name": "FUNCAP - Fundação Cearense de Apoio ao Desenvolvimento Científico e Tecnológico", "url": "https://www.funcap.ce.gov.br"}, "url": "https://ivefac.com.br"}',
            type="application/ld+json",
        ),
        rx.el.style("a[href*='reflex.dev'] { display: none !important; opacity: 0 !important; pointer-events: none !important; visibility: hidden !important; }"),
    ],
)

# Registro das Rotas do Sistema com SEO e OpenGraph
app.add_page(
    home_page,
    route="/",
    on_load=EventoState.carregar_programacao_publica,
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
    on_load=EventoState.carregar_programacao_publica,
    title="Programação Oficial • IV EFAC 2026",
    description="Programação oficial do IV EFAC (11 e 12 de novembro de 2026): conferências magnas, palestras convidadas, minicurso e sessões de apresentação científica.",
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
    title="Acesso e Credencial • IV EFAC 2026",
    description="Acesso ao portal de congressistas e ao painel administrativo do IV EFAC 2026.",
)

app.add_page(
    normas_submissao_page,
    route="/normas-submissao",
    title="Normas de Submissão de Trabalhos • IV EFAC 2026",
    description="Regulamento oficial, diretrizes de formatação (resumo expandido), apresentação em pôster/oral e cronograma de submissões do IV EFAC 2026.",
)
