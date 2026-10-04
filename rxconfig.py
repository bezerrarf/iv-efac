import reflex as rx

config = rx.Config(
    app_name="projeto_web",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                appearance="inherit",
                has_background=True,
                accent_color="indigo",
                radius="large",
            )
        ),
    ],
)