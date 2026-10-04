"""Componente de Malha Gravitacional Interativa (Buraco Negro / Anã Branca)."""

import reflex as rx


def space_fabric_canvas() -> rx.Component:
    """Renderiza a malha do espaço-tempo que reage ao cursor do mouse e ao toque."""
    fabric_js = """
    (function() {
        const canvas = document.getElementById('astro-fabric-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let width = canvas.parentElement.clientWidth || window.innerWidth;
        let height = canvas.parentElement.clientHeight || 500;
        let dpr = Math.min(window.devicePixelRatio || 1, 2);

        function resize() {
            if (!canvas.parentElement) return;
            width = canvas.parentElement.clientWidth || window.innerWidth;
            height = canvas.parentElement.clientHeight || 500;
            canvas.width = width * dpr;
            canvas.height = height * dpr;
            ctx.scale(dpr, dpr);
            initGrid();
        }

        let nodes = [];
        let cols = 0;
        let rows = 0;
        const spacing = width < 768 ? 36 : 48;

        function initGrid() {
            nodes = [];
            cols = Math.ceil(width / spacing) + 1;
            rows = Math.ceil(height / spacing) + 1;
            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const ox = c * spacing;
                    const oy = r * spacing;
                    nodes.push({
                        ox: ox,
                        oy: oy,
                        x: ox,
                        y: oy,
                        vx: 0,
                        vy: 0
                    });
                }
            }
        }

        let mouse = { x: -9999, y: -9999, targetX: -9999, targetY: -9999, active: false };

        function updateMousePos(clientX, clientY) {
            const rect = canvas.getBoundingClientRect();
            mouse.targetX = clientX - rect.left;
            mouse.targetY = clientY - rect.top;
            mouse.active = true;
        }

        window.addEventListener('mousemove', (e) => {
            updateMousePos(e.clientX, e.clientY);
        }, { passive: true });

        window.addEventListener('touchmove', (e) => {
            if (e.touches.length > 0) {
                updateMousePos(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        window.addEventListener('touchend', () => {
            mouse.active = false;
        }, { passive: true });

        document.addEventListener('mouseleave', () => {
            mouse.active = false;
        });

        window.addEventListener('resize', resize, { passive: true });
        resize();

        let time = 0;
        function animate() {
            time += 0.025;
            ctx.clearRect(0, 0, width, height);

            const isDark = document.documentElement.classList.contains('dark');

            // Suaviza a posição do mouse
            if (mouse.active) {
                mouse.x += (mouse.targetX - mouse.x) * 0.15;
                mouse.y += (mouse.targetY - mouse.y) * 0.15;
            } else {
                mouse.x += (-9999 - mouse.x) * 0.1;
                mouse.y += (-9999 - mouse.y) * 0.1;
            }

            const influenceRadius = width < 768 ? 140 : 200;

            // Atualiza física dos nós
            for (let i = 0; i < nodes.length; i++) {
                const n = nodes[i];
                const dx = mouse.x - n.ox;
                const dy = mouse.y - n.oy;
                const dist = Math.sqrt(dx * dx + dy * dy);

                // Ondulação cósmica suave de fundo
                const ambientWave = Math.sin(time + n.ox * 0.012 + n.oy * 0.008) * 3;

                let tx = n.ox;
                let ty = n.oy + ambientWave;

                if (dist < influenceRadius && dist > 1) {
                    const force = (1 - dist / influenceRadius);
                    if (isDark) {
                        // BURACO NEGRO: Atração gravitacional em direção à singularidade do cursor
                        const pull = force * force * 45;
                        tx += (dx / dist) * pull;
                        ty += (dy / dist) * pull;
                    } else {
                        // ANÃ BRANCA: Núcleo ultra-denso radiante com curvatura e leve expansão
                        const warp = Math.sin(force * Math.PI) * 35;
                        tx += (dx / dist) * warp;
                        ty += (dy / dist) * warp;
                    }
                }

                // Elasticidade de retorno
                n.vx = (n.vx + (tx - n.x) * 0.18) * 0.72;
                n.vy = (n.vy + (ty - n.y) * 0.18) * 0.72;
                n.x += n.vx;
                n.y += n.vy;
            }

            // Desenha as linhas do tecido espacial
            ctx.lineWidth = isDark ? 0.9 : 1.1;
            const lineColor = isDark ? 'rgba(56, 189, 248, 0.14)' : 'rgba(31, 111, 196, 0.18)';
            const pointColor = isDark ? 'rgba(129, 140, 248, 0.4)' : 'rgba(74, 158, 47, 0.35)';

            ctx.strokeStyle = lineColor;
            ctx.beginPath();

            for (let r = 0; r < rows; r++) {
                for (let c = 0; c < cols; c++) {
                    const idx = r * cols + c;
                    const n = nodes[idx];

                    // Conexão horizontal
                    if (c < cols - 1) {
                        const rightNode = nodes[idx + 1];
                        ctx.moveTo(n.x, n.y);
                        ctx.lineTo(rightNode.x, rightNode.y);
                    }
                    // Conexão vertical
                    if (r < rows - 1) {
                        const bottomNode = nodes[idx + cols];
                        ctx.moveTo(n.x, n.y);
                        ctx.lineTo(bottomNode.x, bottomNode.y);
                    }
                }
            }
            ctx.stroke();

            // Desenha os pontos de intersecção
            ctx.fillStyle = pointColor;
            for (let i = 0; i < nodes.length; i += 2) {
                const n = nodes[i];
                ctx.fillRect(n.x - 1, n.y - 1, 2, 2);
            }

            // Efeito visual especial na singularidade do cursor
            if (mouse.active && mouse.x > 0 && mouse.y > 0 && mouse.x < width && mouse.y < height) {
                const glow = ctx.createRadialGradient(mouse.x, mouse.y, 0, mouse.x, mouse.y, influenceRadius * 0.8);
                if (isDark) {
                    // Disco de Acreção do Buraco Negro
                    glow.addColorStop(0, 'rgba(56, 189, 248, 0.22)');
                    glow.addColorStop(0.3, 'rgba(147, 51, 234, 0.15)');
                    glow.addColorStop(1, 'transparent');
                } else {
                    // Brilho térmico da Anã Branca
                    glow.addColorStop(0, 'rgba(255, 255, 255, 0.7)');
                    glow.addColorStop(0.2, 'rgba(31, 111, 196, 0.25)');
                    glow.addColorStop(1, 'transparent');
                }
                ctx.fillStyle = glow;
                ctx.beginPath();
                ctx.arc(mouse.x, mouse.y, influenceRadius * 0.8, 0, Math.PI * 2);
                ctx.fill();

                // Núcleo central estelar
                ctx.beginPath();
                ctx.arc(mouse.x, mouse.y, isDark ? 4 : 5, 0, Math.PI * 2);
                ctx.fillStyle = isDark ? '#38bdf8' : '#1f6fc4';
                ctx.fill();
            }

            requestAnimationFrame(animate);
        }

        requestAnimationFrame(animate);
    })();
    """

    return rx.box(
        rx.html(
            f"""
            <canvas id="astro-fabric-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;"></canvas>
            <script>{fabric_js}</script>
            """
        ),
        position="absolute",
        inset="0",
        width="100%",
        height="100%",
        overflow="hidden",
        pointer_events="none",
        z_index="1",
    )
