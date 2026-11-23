import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="For You ✨",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
        #MainMenu, footer, header, .stDeployButton {visibility: hidden !important;}
        .stApp {
            background-color: #07040e;
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
    <title>For You ✨</title>
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
            background: radial-gradient(circle at 50% 35%, #190c2e 0%, #07040e 75%);
            font-family: 'Georgia', serif;
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
            background: radial-gradient(circle at center, rgba(35, 15, 58, 0.92) 0%, rgba(7, 4, 14, 0.98) 100%);
            z-index: 20;
            transition: opacity 1s ease, visibility 1s ease;
            cursor: pointer;
            text-align: center;
            padding: 24px;
        }
        #overlay.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        .pulse-heart {
            font-size: 3.6rem;
            margin-bottom: 16px;
            animation: pulse 1.5s infinite ease-in-out;
            filter: drop-shadow(0 0 18px rgba(255, 120, 185, 0.85));
        }
        .tap-title {
            color: #ffe6f0;
            font-size: 1.45rem;
            font-style: italic;
            letter-spacing: 1.5px;
            text-shadow: 0 0 14px rgba(255, 150, 200, 0.7);
        }
        .tap-sub {
            color: #cbb2ff;
            font-size: 0.9rem;
            margin-top: 10px;
            opacity: 0.85;
        }
        #hud {
            position: fixed;
            top: 24px;
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            max-width: 680px;
            text-align: center;
            pointer-events: none;
            z-index: 10;
        }
        #top-name {
            color: #ffd6e7;
            font-size: clamp(1.3rem, 3.5vw, 2rem);
            font-style: italic;
            letter-spacing: 3px;
            margin-bottom: 6px;
            opacity: 0;
            transition: opacity 1.5s ease;
            text-shadow: 0 0 16px rgba(255, 130, 190, 0.8);
        }
        #top-name.show {
            opacity: 1;
        }
        #quote {
            color: #ffffff;
            font-size: clamp(1rem, 2.8vw, 1.45rem);
            font-style: italic;
            letter-spacing: 1px;
            min-height: 1.8rem;
            text-shadow: 0 0 14px rgba(255, 155, 210, 0.85), 0 0 28px rgba(185, 125, 255, 0.55);
        }
        #bottom-bar {
            position: fixed;
            bottom: 18px;
            left: 50%;
            transform: translateX(-50%);
            width: 92%;
            text-align: center;
            pointer-events: none;
            z-index: 10;
            opacity: 0;
            transition: opacity 1.4s ease;
        }
        #bottom-bar.show {
            opacity: 1;
        }
        #sub-msg {
            color: #f8bbd0;
            font-size: 0.95rem;
            font-style: italic;
            text-shadow: 0 0 10px rgba(255, 128, 171, 0.6);
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.16); }
        }
    </style>
</head>
<body>
    <div id="overlay">
        <div class="pulse-heart">✨💖✨</div>
        <div class="tap-title">Tap anywhere to begin...</div>
        <div class="tap-sub">Watch the stars fall &amp; touch the screen for magic</div>
    </div>

    <div id="hud">
        <div id="top-name">For You</div>
        <div id="quote"></div>
    </div>

    <div id="bottom-bar">
        <div id="sub-msg"></div>
    </div>

    <canvas id="canvas"></canvas>

    <script>
        // ======================================================
        // CUSTOMIZE YOUR TEXT HERE:
        const TOP_TITLE = "Us ✨";
        const MAIN_QUOTE = "May Our Love Never End...";
        const BOTTOM_NOTE = "Tap or drag anywhere to send hearts & stardust 💖";
        // ======================================================

        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('overlay');
        const topNameEl = document.getElementById('top-name');
        const quoteEl = document.getElementById('quote');
        const bottomBar = document.getElementById('bottom-bar');
        const subMsgEl = document.getElementById('sub-msg');

        let W = canvas.width = window.innerWidth;
        let H = canvas.height = window.innerHeight;

        let started = false;
        let quoteTriggered = false;
        let frame = 0;

        let particles = [];
        let stars = [];
        let bursts = [];
        let hearts = [];

        const PALETTE = ['#ff9ecb', '#ffc4e1', '#d2b4ff', '#ffffff', '#ff77ad', '#ffe0f0'];

        // Background ambient starfield
        function createStars() {
            stars = [];
            const n = Math.min(180, Math.floor((W * H) / 6000));
            for (let i = 0; i < n; i++) {
                stars.push({
                    x: Math.random() * W,
                    y: Math.random() * H,
                    r: Math.random() * 1.5 + 0.3,
                    phase: Math.random() * Math.PI * 2,
                    spd: Math.random() * 0.025 + 0.008
                });
            }
        }
        createStars();

        // Soft chime on first tap
        function playChime() {
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const ac = new AudioContext();
                const freqs = [523.25, 659.25, 783.99, 987.77, 1174.66];
                freqs.forEach((f, idx) => {
                    const osc = ac.createOscillator();
                    const gain = ac.createGain();
                    osc.type = 'sine';
                    const t = ac.currentTime + idx * 0.22;
                    osc.frequency.setValueAtTime(f, t);
                    gain.gain.setValueAtTime(0.0001, t);
                    gain.gain.exponentialRampToValueAtTime(0.06, t + 0.08);
                    gain.gain.exponentialRampToValueAtTime(0.0001, t + 2.0);
                    osc.connect(gain);
                    gain.connect(ac.destination);
                    osc.start(t);
                    osc.stop(t + 2.1);
                });
            } catch (e) {}
        }

        // Build a clear, graceful romantic couple outline + heart on an offscreen canvas
        function sampleCouplePoints() {
            const size = 600;
            const off = document.createElement('canvas');
            off.width = size;
            off.height = size;
            const octx = off.getContext('2d');

            octx.strokeStyle = '#ffffff';
            octx.lineWidth = 4.2;
            octx.lineCap = 'round';
            octx.lineJoin = 'round';

            // 1. TALLER PARTNER (Left, leaning forward toward forehead/cheek)
            octx.beginPath();
            // Hair crown & swept bangs
            octx.moveTo(185, 225);
            octx.bezierCurveTo(165, 165, 195, 105, 255, 98);
            octx.bezierCurveTo(305, 92, 342, 128, 345, 175);
            // Hair strands
            octx.moveTo(205, 135);
            octx.bezierCurveTo(240, 112, 295, 115, 325, 148);
            octx.moveTo(220, 162);
            octx.bezierCurveTo(255, 142, 300, 145, 322, 172);
            // Forehead, nose bridge, tip, lips, chin
            octx.moveTo(345, 175);
            octx.lineTo(354, 198); // forehead/brow
            octx.lineTo(366, 216); // nose
            octx.lineTo(352, 222); // under nose
            octx.lineTo(358, 229); // upper lip
            octx.lineTo(351, 235); // lip line
            octx.lineTo(357, 242); // lower lip
            octx.quadraticCurveTo(348, 260, 324, 262); // chin & jaw
            // Neck & shoulders/coat
            octx.quadraticCurveTo(295, 262, 282, 248);
            octx.moveTo(286, 256);
            octx.quadraticCurveTo(288, 300, 272, 335);
            octx.quadraticCurveTo(220, 355, 165, 445);
            // Back/shoulder
            octx.moveTo(185, 225);
            octx.quadraticCurveTo(168, 275, 152, 345);
            octx.quadraticCurveTo(132, 395, 122, 445);
            // Ear
            octx.moveTo(242, 202);
            octx.quadraticCurveTo(228, 202, 230, 226);
            octx.quadraticCurveTo(234, 236, 244, 232);
            octx.stroke();

            // 2. PARTNER IN FRONT (Right, head tilted back slightly)
            octx.beginPath();
            // Hair bun & head contour
            octx.moveTo(342, 258);
            octx.bezierCurveTo(375, 245, 412, 265, 418, 302);
            octx.bezierCurveTo(422, 335, 395, 362, 365, 365);
            // Hair bun at back right
            octx.moveTo(412, 282);
            octx.bezierCurveTo(448, 278, 462, 312, 438, 338);
            octx.bezierCurveTo(422, 352, 405, 342, 412, 325);
            // Face profile (forehead, nose, lips, chin)
            octx.moveTo(342, 258);
            octx.quadraticCurveTo(322, 272, 316, 294); // forehead
            octx.lineTo(304, 308); // nose
            octx.lineTo(315, 314); // nose tip
            octx.lineTo(310, 321); // lips
            octx.lineTo(318, 329); // chin
            octx.quadraticCurveTo(332, 346, 354, 345); // jawline
            // Closed serene eye
            octx.moveTo(322, 296);
            octx.quadraticCurveTo(330, 301, 337, 296);
            // Neck & shoulder/dress curve
            octx.moveTo(342, 345);
            octx.quadraticCurveTo(340, 378, 352, 402);
            octx.quadraticCurveTo(405, 415, 445, 465);
            octx.moveTo(316, 340);
            octx.quadraticCurveTo(306, 382, 285, 412);
            octx.quadraticCurveTo(245, 432, 225, 465);
            octx.stroke();

            // 3. CUTE HEART ABOVE THEM
            octx.beginPath();
            const hx = 435, hy = 185, s = 18;
            octx.moveTo(hx, hy + s * 0.35);
            octx.bezierCurveTo(hx, hy - s * 0.45, hx - s, hy - s * 0.45, hx - s, hy + s * 0.25);
            octx.bezierCurveTo(hx - s, hy + s * 0.95, hx, hy + s * 1.35, hx, hy + s * 1.65);
            octx.bezierCurveTo(hx, hy + s * 1.35, hx + s, hy + s * 0.95, hx + s, hy + s * 0.25);
            octx.bezierCurveTo(hx + s, hy - s * 0.45, hx, hy - s * 0.45, hx, hy + s * 0.35);
            octx.stroke();

            const data = octx.getImageData(0, 0, size, size).data;
            const pts = [];
            const step = 3;

            const scale = Math.min(W * 0.85, H * 0.62) / size;
            const ox = (W - size * scale) / 2;
            const oy = (H - size * scale) / 2 + H * 0.05;

            for (let y = 0; y < size; y += step) {
                for (let x = 0; x < size; x += step) {
                    if (data[(y * size + x) * 4 + 3] > 120) {
                        pts.push({
                            tx: ox + x * scale + (Math.random() - 0.5) * 2,
                            ty: oy + y * scale + (Math.random() - 0.5) * 2
                        });
                    }
                }
            }
            return pts;
        }

        function initParticles(repositionOnly = false) {
            const targets = sampleCouplePoints();
            targets.sort(() => Math.random() - 0.5);

            particles = targets.map((pt, idx) => {
                const prev = particles[idx];
                return {
                    x: repositionOnly && prev ? prev.x : Math.random() * W,
                    y: repositionOnly && prev ? prev.y : -30 - Math.random() * H * 0.9,
                    tx: pt.tx,
                    ty: pt.ty,
                    vx: (Math.random() - 0.5) * 2.5,
                    vy: Math.random() * 2 + 1.5,
                    r: Math.random() * 1.7 + 1.1,
                    color: PALETTE[idx % PALETTE.length],
                    delay: repositionOnly ? 0 : Math.floor((idx / targets.length) * 150),
                    phase: Math.random() * Math.PI * 2,
                    twinkleStar: idx % 9 === 0
                };
            });
        }

        function typeText(str, element, speed = 75) {
            element.textContent = '';
            let i = 0;
            const timer = setInterval(() => {
                element.textContent += str.charAt(i);
                i++;
                if (i >= str.length) {
                    clearInterval(timer);
                    subMsgEl.textContent = BOTTOM_NOTE;
                    bottomBar.classList.add('show');
                }
            }, speed);
        }

        function addMagicAt(x, y) {
            for (let i = 0; i < 28; i++) {
                const ang = Math.random() * Math.PI * 2;
                const spd = Math.random() * 5 + 1.2;
                bursts.push({
                    x, y,
                    vx: Math.cos(ang) * spd,
                    vy: Math.sin(ang) * spd - 1.2,
                    alpha: 1,
                    decay: 0.015 + Math.random() * 0.015,
                    r: Math.random() * 2.6 + 1.1,
                    color: PALETTE[Math.floor(Math.random() * PALETTE.length)]
                });
            }
            hearts.push({
                x, y,
                vx: (Math.random() - 0.5) * 1.4,
                vy: -1.5 - Math.random() * 1.1,
                alpha: 1,
                size: 8 + Math.random() * 6
            });
        }

        function drawHeart(x, y, s, alpha) {
            ctx.save();
            ctx.globalAlpha = Math.max(0, alpha);
            ctx.fillStyle = '#ff7eb6';
            ctx.shadowColor = '#ff4794';
            ctx.shadowBlur = 12;
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.bezierCurveTo(x, y - s * 0.5, x - s, y - s * 0.5, x - s, y + s * 0.2);
            ctx.bezierCurveTo(x - s, y + s * 0.9, x, y + s * 1.25, x, y + s * 1.55);
            ctx.bezierCurveTo(x, y + s * 1.25, x + s, y + s * 0.9, x + s, y + s * 0.2);
            ctx.bezierCurveTo(x + s, y - s * 0.5, x, y - s * 0.5, x, y);
            ctx.fill();
            ctx.restore();
        }

        function drawCrossSparkle(x, y, r, alpha) {
            ctx.save();
            ctx.globalAlpha = Math.max(0, alpha);
            ctx.strokeStyle = '#ffffff';
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(x - r * 2.5, y);
            ctx.lineTo(x + r * 2.5, y);
            ctx.moveTo(x, y - r * 2.5);
            ctx.lineTo(x, y + r * 2.5);
            ctx.stroke();
            ctx.restore();
        }

        function loop() {
            frame++;
            ctx.fillStyle = 'rgba(7, 4, 14, 0.24)';
            ctx.fillRect(0, 0, W, H);

            // Background stars
            for (const st of stars) {
                st.phase += st.spd;
                const a = 0.2 + Math.abs(Math.sin(st.phase)) * 0.7;
                ctx.fillStyle = `rgba(255, 242, 250, ${a})`;
                ctx.beginPath();
                ctx.arc(st.x, st.y, st.r, 0, Math.PI * 2);
                ctx.fill();
            }

            if (started) {
                let settled = 0;

                for (let i = 0; i < particles.length; i++) {
                    const p = particles[i];
                    if (p.delay > 0) {
                        p.delay--;
                        continue;
                    }

                    const dx = p.tx - p.x;
                    const dy = p.ty - p.y;
                    const dist = Math.hypot(dx, dy);

                    if (dist < 2.0) {
                        settled++;
                        p.x = p.tx + Math.sin(frame * 0.045 + p.phase) * 0.75;
                        p.y = p.ty + Math.cos(frame * 0.045 + p.phase) * 0.75;
                    } else {
                        p.vx = p.vx * 0.89 + dx * 0.048;
                        p.vy = p.vy * 0.89 + dy * 0.048 + 0.12;
                        p.x += p.vx;
                        p.y += p.vy;
                    }

                    const glow = 0.65 + Math.sin(frame * 0.09 + p.phase) * 0.35;
                    ctx.globalAlpha = glow;
                    ctx.fillStyle = p.color;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                    ctx.fill();

                    if (p.twinkleStar && glow > 0.9) {
                        drawCrossSparkle(p.x, p.y, p.r * 1.4, glow);
                    }
                    ctx.globalAlpha = 1;
                }

                if (!quoteTriggered && particles.length > 0 && settled > particles.length * 0.65) {
                    quoteTriggered = true;
                    topNameEl.textContent = TOP_TITLE;
                    topNameEl.classList.add('show');
                    typeText(MAIN_QUOTE, quoteEl, 75);
                }
            }

            // Touch bursts
            for (let i = bursts.length - 1; i >= 0; i--) {
                const b = bursts[i];
                b.x += b.vx;
                b.y += b.vy;
                b.vy += 0.07;
                b.alpha -= b.decay;
                if (b.alpha <= 0) {
                    bursts.splice(i, 1);
                    continue;
                }
                ctx.globalAlpha = b.alpha;
                ctx.fillStyle = b.color;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.r, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            // Floating hearts
            for (let i = hearts.length - 1; i >= 0; i--) {
                const h = hearts[i];
                h.x += h.vx;
                h.y += h.vy;
                h.alpha -= 0.011;
                if (h.alpha <= 0) {
                    hearts.splice(i, 1);
                    continue;
                }
                drawHeart(h.x, h.y, h.size, h.alpha);
            }

            requestAnimationFrame(loop);
        }

        function handleStart(e) {
            if (!started) {
                started = true;
                overlay.classList.add('hidden');
                playChime();
                initParticles(false);
            }
            const pt = e.touches ? e.touches[0] : e;
            if (pt && typeof pt.clientX === 'number') {
                addMagicAt(pt.clientX, pt.clientY);
            }
        }

        overlay.addEventListener('click', handleStart);
        overlay.addEventListener('touchstart', handleStart, { passive: true });

        canvas.addEventListener('click', (e) => {
            if (started) addMagicAt(e.clientX, e.clientY);
        });
        canvas.addEventListener('touchmove', (e) => {
            if (started && e.touches[0] && Math.random() < 0.4) {
                addMagicAt(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        window.addEventListener('resize', () => {
            W = canvas.width = window.innerWidth;
            H = canvas.height = window.innerHeight;
            createStars();
            if (started) initParticles(true);
        });

        loop();
    </script>
</body>
</html>
"""

components.html(html_code, height=950, scrolling=False)
