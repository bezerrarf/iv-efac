import os
import reflex as rx

# Desativa o pre-render SSR/SSG no build de producao para evitar timeout do React Router em VMs enxutas (e2-micro)
os.environ.setdefault("REFLEX_SSR", "false")

config = rx.Config(
    app_name="projeto_web",
    deploy_url="https://ivefac.com.br",
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

