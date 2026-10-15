import reflex as rx
from projeto_web.state.auth_state import AuthState


def feedback_alert() -> rx.Component:
    return rx.cond(
        AuthState.feedback_msg != "",
        rx.box(
            rx.callout(
                AuthState.feedback_msg,
                icon=rx.cond(AuthState.feedback_tipo == "success", "circle-check", "alert-circle"),
                color_scheme=rx.cond(AuthState.feedback_tipo == "success", "green", "red"),
                variant="soft",
                size="2",
                width="100%",
                cursor="pointer",
                on_click=AuthState.limpar_feedback,
            ),
            rx.button(
                id="btn-auto-dismiss-feedback",
                on_click=AuthState.limpar_feedback,
                display="none",
            ),
            rx.script("""
            (function() {
                var banner = document.getElementById("top-feedback-banner");
                var btn = document.getElementById("btn-auto-dismiss-feedback");
                if (!banner || !btn) return;

                var dismissed = false;
                function dismiss() {
                    if (dismissed) return;
                    dismissed = true;
                    cleanupListeners();
                    banner.style.transition = "opacity 0.35s ease, max-height 0.35s ease, margin 0.35s ease";
                    banner.style.opacity = "0";
                    banner.style.maxHeight = "0px";
                    banner.style.marginBottom = "0px";
                    banner.style.overflow = "hidden";
                    setTimeout(function() {
                        if (btn) btn.click();
                    }, 350);
                }

                function onUserInteract() {
                    dismiss();
                }

                function cleanupListeners() {
                    window.removeEventListener("scroll", onUserInteract);
                    window.removeEventListener("click", onUserInteract);
                    window.removeEventListener("keydown", onUserInteract);
                    window.removeEventListener("touchstart", onUserInteract);
                }

                // Auto-dismiss ap?s no m?ximo 10 segundos
                var timer = setTimeout(dismiss, 10000);

                // Espera 350ms antes de registrar listeners para n?o capturar o clique inicial que gerou a mensagem
                setTimeout(function() {
                    if (dismissed) return;
                    window.addEventListener("scroll", onUserInteract, { once: true, passive: true });
                    window.addEventListener("click", onUserInteract, { once: true, capture: true });
                    window.addEventListener("keydown", onUserInteract, { once: true, passive: true });
                    window.addEventListener("touchstart", onUserInteract, { once: true, passive: true });
                }, 350);
            })();
            """),
            id="top-feedback-banner",
            width="100%",
            margin_bottom="1rem",
        ),
    )
