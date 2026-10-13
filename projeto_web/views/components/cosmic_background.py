"""Plano de Fundo Vetorial Cósmico Responsivo (UI/UX Pro Max).
Substitui a malha quântica JS por um container SVG adaptável de altíssimo desempenho.
Utiliza a arte oficial do Cariri Cósmico (Chapada do Araripe & Astrofísica) com visibilidade ampliada.
"""

import reflex as rx


def cosmic_background() -> rx.Component:
    """Fundo em camada fixa com escala vetorial preservada (preserveAspectRatio='xMidYMid slice')
    e vinhetas suaves permitindo visualização nítida e vibrante do céu estrelado e da Chapada do Araripe.
    """
    return rx.box(
        rx.html(
            """
            <div style="position: fixed; inset: 0; width: 100vw; height: 100vh; overflow: hidden; pointer-events: none; z-index: 0;">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 1920 1080"
                    preserveAspectRatio="xMidYMid slice"
                    style="position: absolute; inset: 0; width: 100%; height: 100%;"
                >
                    <defs>
                        <!-- Degradê atmosférico cósmico sutil para garantir legibilidade dos textos sem encobrir a arte -->
                        <linearGradient id="cosmic-vignette" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#060814" stop-opacity="0.35" />
                            <stop offset="30%" stop-color="#060814" stop-opacity="0.15" />
                            <stop offset="70%" stop-color="#060814" stop-opacity="0.25" />
                            <stop offset="100%" stop-color="#060814" stop-opacity="0.55" />
                        </linearGradient>

                        <!-- Nebulosa Ciano Difusa Suave -->
                        <radialGradient id="nebula-cyan" cx="20%" cy="25%" r="45%">
                            <stop offset="0%" stop-color="#00ADB5" stop-opacity="0.20" />
                            <stop offset="60%" stop-color="#00ADB5" stop-opacity="0.04" />
                            <stop offset="100%" stop-color="#060814" stop-opacity="0" />
                        </radialGradient>

                        <!-- Nebulosa Índigo Difusa Suave -->
                        <radialGradient id="nebula-indigo" cx="80%" cy="40%" r="50%">
                            <stop offset="0%" stop-color="#6366F1" stop-opacity="0.18" />
                            <stop offset="65%" stop-color="#6366F1" stop-opacity="0.03" />
                            <stop offset="100%" stop-color="#060814" stop-opacity="0" />
                        </radialGradient>
                    </defs>

                    <!-- Imagem Oficial Base: Chapada do Araripe, Pesquisadores & Cosmos -->
                    <image
                        href="/fundo_cosmico.jpeg"
                        x="0"
                        y="0"
                        width="1920"
                        height="1080"
                        preserveAspectRatio="xMidYMid slice"
                    />

                    <!-- Camadas de Amortecimento Atmosférico Leve -->
                    <rect width="100%" height="100%" fill="url(#nebula-cyan)" />
                    <rect width="100%" height="100%" fill="url(#nebula-indigo)" />
                    <rect width="100%" height="100%" fill="url(#cosmic-vignette)" />
                </svg>
            </div>
            """
        ),
        position="fixed",
        inset="0",
        width="100vw",
        height="100vh",
        pointer_events="none",
        z_index="0",
    )
