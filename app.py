import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="I Love You 💖",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        .stApp {
            background-color: #000000;
            overflow: hidden;
        }
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            display: block;
            border: none;
            width: 100vw;
            height: 100vh;
        }
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>I Love You 💖</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            user-select: none;
            -webkit-tap-highlight-color: transparent;
        }
        html, body {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #000000;
            font-family: Arial, Helvetica, sans-serif;
        }
        canvas {
            display: block;
            width: 100vw;
            height: 100vh;
        }
        #overlay {
            position: fixed;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #000000;
            z-index: 20;
            transition: opacity 0.8s ease, visibility 0.8s ease;
            cursor: pointer;
            text-align: center;
            padding: 20px;
        }
        #overlay.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        .heart-icon {
            font-size: 3.4rem;
            margin-bottom: 14px;
            animation: beat 1.2s infinite ease-in-out;
        }
        .tap-label {
            color: #ffb6c1;
            font-size: 1.25rem;
            font-weight: bold;
            letter-spacing: 1px;
        }
        @keyframes beat {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.18); }
        }
    </style>
</head>
<body>
    <div id="overlay">
        <div class="heart-icon">💖</div>
        <div class="tap-label">Tap to open...</div>
    </div>

    <canvas id="canvas"></canvas>

    <script>
        // ======================================================
        // CUSTOMIZE THE REPEATED TEXT HERE:
        const PHRASE = "I love you";
        const PINK_COLOR = "#ffb6c1";
        // ======================================================

        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('overlay');

        let W = canvas.width = window.innerWidth;
        let H = canvas.height = window.innerHeight;

        let started = false;
        let labels = [];
        let drawIndex = 0;
        let bursts = [];

        // Parametric heart formula matching classic Python turtle heart scripts
        function heartPoint(t, scale) {
            const x = 16 * Math.pow(Math.sin(t), 3);
            const y = -(
                13 * Math.cos(t) -
                5 * Math.cos(2 * t) -
                2 * Math.cos(3 * t) -
                Math.cos(4 * t)
            );
            return { x: x * scale, y: y * scale };
        }

        function buildHeartLabels() {
            labels = [];
            drawIndex = 0;

            const baseScale = Math.min(W, H) / 42;
            const cx = W / 2;
            const cy = H / 2 - H * 0.02;
            const steps = 120;

            // Concentric heart layers from outer edge inward
            for (let layer = 16; layer >= 10; layer -= 1.2) {
                const s = baseScale * (layer / 14.5);
                for (let i = 0; i < steps; i++) {
                    const t = (i * Math.PI * 2) / steps;
                    const pt = heartPoint(t, s);
                    labels.push({
                        x: cx + pt.x,
                        y: cy + pt.y,
                        alpha: 0,
                        fontSize: Math.max(8, Math.min(11, Math.round(baseScale * 0.85)))
                    });
                }
            }
        }

        function spawnBurst(x, y) {
            for (let i = 0; i < 18; i++) {
                const angle = (Math.PI * 2 * i) / 18;
                const speed = 1.5 + Math.random() * 3;
                bursts.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    life: 1,
                    text: i % 3 === 0 ? "💖" : PHRASE
                });
            }
        }

        function render() {
            ctx.fillStyle = "#000000";
            ctx.fillRect(0, 0, W, H);

            if (started) {
                // Reveal "I love you" labels progressively like turtle drawing
                const revealPerFrame = 4;
                if (drawIndex < labels.length) {
                    drawIndex = Math.min(labels.length, drawIndex + revealPerFrame);
                }

                ctx.textAlign = "center";
                ctx.textBaseline = "middle";

                for (let i = 0; i < drawIndex; i++) {
                    const item = labels[i];
                    if (item.alpha < 1) {
                        item.alpha = Math.min(1, item.alpha + 0.12);
                    }
                    ctx.save();
                    ctx.globalAlpha = item.alpha;
                    ctx.fillStyle = PINK_COLOR;
                    ctx.font = `bold ${item.fontSize}px Arial, sans-serif`;
                    ctx.fillText(PHRASE, item.x, item.y);
                    ctx.restore();
                }
            }

            // Draw tap bursts
            for (let i = bursts.length - 1; i >= 0; i--) {
                const b = bursts[i];
                b.x += b.vx;
                b.y += b.vy;
                b.life -= 0.025;
                if (b.life <= 0) {
                    bursts.splice(i, 1);
                    continue;
                }
                ctx.save();
                ctx.globalAlpha = b.life;
                ctx.fillStyle = PINK_COLOR;
                ctx.font = "bold 11px Arial, sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(b.text, b.x, b.y);
                ctx.restore();
            }

            requestAnimationFrame(render);
        }

        function startHeart(e) {
            if (!started) {
                started = true;
                overlay.classList.add('hidden');
                buildHeartLabels();
            }
            const clientX = e.touches && e.touches[0] ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches && e.touches[0] ? e.touches[0].clientY : e.clientY;
            if (typeof clientX === "number" && typeof clientY === "number") {
                spawnBurst(clientX, clientY);
            }
        }

        overlay.addEventListener('click', startHeart);
        overlay.addEventListener('touchstart', startHeart, { passive: true });

        canvas.addEventListener('click', (e) => {
            if (started) spawnBurst(e.clientX, e.clientY);
        });
        canvas.addEventListener('touchstart', (e) => {
            if (started && e.touches[0]) {
                spawnBurst(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        window.addEventListener('resize', () => {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            if (started) {
                buildHeartLabels();
                drawIndex = labels.length;
                labels.forEach(item => { item.alpha = 1; });
            }
        });

        render();
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
