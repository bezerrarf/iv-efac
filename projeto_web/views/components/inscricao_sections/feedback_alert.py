import reflex as rx
from projeto_web.state.evento_state import EventoState
from projeto_web.state.auth_state import AuthState
from projeto_web.styles.theme import *

def feedback_alert() -> rx.Component:
    return rx.cond(
        AuthState.feedback_msg != "",
        rx.callout(
            AuthState.feedback_msg,
            icon=rx.cond(AuthState.feedback_tipo == "success", "circle-check", "alert-circle"),
            color_scheme=rx.cond(AuthState.feedback_tipo == "success", "green", "red"),
            variant="soft",
            size="2",
            width="100%",
            margin_bottom="1rem",
        ),
    )


