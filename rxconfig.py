import os
import reflex as rx

# Desativa o pre-render SSR/SSG no build de producao para evitar timeout do React Router em VMs enxutas (e2-micro)
os.environ.setdefault("REFLEX_SSR", "false")

config = rx.Config(
    app_name="projeto_web",
    deploy_url="https://ivefac.com.br",
    backend_host="0.0.0.0",
    cors_allowed_origins=[
        "*",
        "https://ivefac.com.br",
        "http://ivefac.com.br",
        "https://www.ivefac.com.br",
        "http://www.ivefac.com.br",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    show_built_with_reflex=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="dark",
                has_background=False,
                accent_color="cyan",
                radius="large",
            )
        ),
    ],
)

