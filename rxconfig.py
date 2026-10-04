import reflex as rx

config = rx.Config(
    app_name="projeto_web",
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
