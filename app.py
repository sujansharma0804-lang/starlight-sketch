import streamlit as st
import streamlit.components.v1 as components

# Configure full-screen clean mobile view
st.set_page_config(
    page_title="For You ✨",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header, footer, and padding for an immersive full-screen feel
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
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
        body, html {
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #08050f;
            font-family: 'Georgia', serif;
        }
        canvas {
            display: block;
            width: 100%;
            height: 100%;
        }
        #overlay {
            position: absolute;
            inset: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: radial-gradient(circle at center, rgba(25, 12, 40, 0.85) 0%, #08050f 100%);
            z-index: 10;
            transition: opacity 1.2s ease, visibility 1.2s ease;
            cursor: pointer;
            text-align: center;
            padding: 20px;
        }
        #overlay.hidden {
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
        }
        .pulse-heart {
            font-size: 3.5rem;
            margin-bottom: 18px;
            animation: pulse 1.6s infinite ease-in-out;
            filter: drop-shadow(0 0 15px rgba(255, 130, 180, 0.7));
        }
        .tap-text {
            color: #fce4ec;
            font-size: 1.35rem;
            letter-spacing: 2px;
            font-style: italic;
            text-shadow: 0 0 12px rgba(255, 182, 193, 0.6);
        }
        .sub-text {
            color: #b39ddb;
            font-size: 0.85rem;
            margin-top: 10px;
            letter-spacing: 1px;
            opacity: 0.8;
        }
        #quote-container {
            position: absolute;
            top: 8%;
            left: 50%;
            transform: translateX(-50%);
            width: 90%;
            text-align: center;
            pointer-events: none;
            z-index: 5;
        }
        #quote {
            color: #fff0f5;
            font-size: clamp(1.2rem, 4vw, 1.85rem);
            font-style: italic;
            letter-spacing: 1.5px;
            text-shadow: 0 0 15px rgba(255, 140, 190, 0.85), 0 0 30px rgba(200, 130, 255, 0.5);
            min-height: 2.2rem;
        }
        #bottom-hint {
            position: absolute;
            bottom: 5%;
            left: 50%;
            transform: translateX(-50%);
            color: rgba(248, 187, 208, 0.75);
            font-size: 0.9rem;
            font-style: italic;
            letter-spacing: 1px;
            opacity: 0;
            transition: opacity 1.5s ease;
            pointer-events: none;
            text-align: center;
            width: 90%;
        }
        #bottom-hint.visible {
            opacity: 1;
        }
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.18); }
        }
    </style>
</head>
<body>

    <div id="overlay">
        <div class="pulse-heart">✨💖✨</div>
        <div class="tap-text">Tap anywhere to open...</div>
        <div class="sub-text">(Turn your sound on for a little magic)</div>
    </div>

    <div id="quote-container">
        <div id="quote"></div>
    </div>

    <div id="bottom-hint">Touch anywhere on the screen to send sparkles ✨</div>

    <canvas id="scene"></canvas>

    <script>
        // ==========================================
        // CUSTOMIZE YOUR MESSAGE HERE:
        const ROMANTIC_QUOTE = "May Our Love Never End...";
        const SUB_MESSAGE = "Every little piece of me falls for you ✨";
        // ==========================================

        const canvas = document.getElementById('scene');
        const ctx = canvas.getContext('2d');
        const overlay = document.getElementById('overlay');
        const quoteEl = document.getElementById('quote');
        const bottomHint = document.getElementById('bottom-hint');

        let width, height;
        let particles = [];
        let bgStars = [];
        let touchBursts = [];
        let floatingHearts = [];
        let started = false;
        let quoteStarted = false;

        const COLORS = [
            '#ff9ec6', // soft rose pink
            '#ffc2e2', // pastel pink
            '#c8a2ff', // lavender
            '#ffffff', // pure starlight white
            '#ff7eb3'  // warm coral pink
        ];

        function resize() {
            width = canvas.width = window.innerWidth;
            height = canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', () => {
            resize();
            if (started) buildTargets(true);
        });
        resize();

        // Ambient twinkling background stars
        function initStars() {
            bgStars = [];
            const count = Math.floor((width * height) / 7000);
            for (let i = 0; i < count; i++) {
                bgStars.push({
                    x: Math.random() * width,
                    y: Math.random() * height,
                    r: Math.random() * 1.4 + 0.3,
                    alpha: Math.random(),
                    speed: Math.random() * 0.02 + 0.005
                });
            }
        }
        initStars();

        // Gentle Web Audio chime when opened (no external MP3 needed!)
        function playRomanticChime() {
            try {
                const AudioCtx = window.AudioContext || window.webkitAudioContext;
                const audioCtx = new AudioCtx();
                const notes = [523.25, 659.25, 783.99, 987.77, 1046.50]; // Cmaj9 arpeggio
                notes.forEach((freq, idx) => {
                    const osc = audioCtx.createOscillator();
                    const gain = audioCtx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime + idx * 0.28);
                    gain.gain.setValueAtTime(0.001, audioCtx.currentTime + idx * 0.28);
                    gain.gain.exponentialRampToValueAtTime(0.08, audioCtx.currentTime + idx * 0.28 + 0.1);
                    gain.gain.exponentialRampToValueAtTime(0.0001, audioCtx.currentTime + idx * 0.28 + 2.2);
                    osc.connect(gain);
                    gain.connect(audioCtx.destination);
                    osc.start(audioCtx.currentTime + idx * 0.28);
                    osc.stop(audioCtx.currentTime + idx * 0.28 + 2.3);
                });
            } catch (e) {}
        }

        // Draw the romantic couple line art onto an offscreen canvas to sample particle coordinates
        function getCoupleCoordinates() {
            const offCanvas = document.createElement('canvas');
            const offCtx = offCanvas.getContext('2d');
            const size = 500;
            offCanvas.width = size;
            offCanvas.height = size;

            offCtx.strokeStyle = '#ffffff';
            offCtx.lineWidth = 3.2;
            offCtx.lineCap = 'round';
            offCtx.lineJoin = 'round';

            // --- HIS SILHOUETTE (Left/Top, kissing her forehead) ---
            offCtx.beginPath();
            // Hair & forehead
            offCtx.moveTo(145, 215);
            offCtx.bezierCurveTo(115, 175, 135, 105, 195, 85);
            offCtx.bezierCurveTo(235, 72, 285, 88, 305, 125);
            offCtx.bezierCurveTo(322, 152, 315, 180, 298, 198);
            // Swept hair locks
            offCtx.moveTo(165, 130);
            offCtx.bezierCurveTo(195, 102, 250, 105, 280, 138);
            offCtx.moveTo(185, 155);
            offCtx.bezierCurveTo(215, 132, 255, 135, 272, 160);
            // Brow, nose, lips kissing her forehead
            offCtx.moveTo(298, 198);
            offCtx.quadraticCurveTo(306, 215, 294, 226); // nose
            offCtx.quadraticCurveTo(302, 234, 292, 242); // upper lip
            offCtx.quadraticCurveTo(298, 250, 285, 258); // lower lip & chin
            // Jawline & neck
            offCtx.quadraticCurveTo(255, 268, 232, 252);
            offCtx.moveTo(175, 235);
            offCtx.quadraticCurveTo(185, 295, 168, 355);
            // Shoulder / back
            offCtx.moveTo(145, 215);
            offCtx.bezierCurveTo(125, 245, 122, 295, 115, 375);
            // Ear detail
            offCtx.moveTo(205, 195);
            offCtx.bezierCurveTo(192, 190, 190, 218, 205, 220);
            offCtx.stroke();

            // --- HER SILHOUETTE (Right/Bottom, tilted up) ---
            offCtx.beginPath();
            // Forehead, nose, lips, chin
            offCtx.moveTo(275, 235);
            offCtx.quadraticCurveTo(305, 245, 318, 272); // forehead
            offCtx.quadraticCurveTo(334, 288, 322, 298); // nose
            offCtx.quadraticCurveTo(328, 306, 318, 312); // upper lip
            offCtx.quadraticCurveTo(324, 320, 312, 328); // lower lip
            offCtx.quadraticCurveTo(304, 344, 282, 342); // chin
            // Closed happy eye & lashes
            offCtx.moveTo(292, 278);
            offCtx.quadraticCurveTo(302, 284, 310, 278);
            // Neck & collarbone
            offCtx.moveTo(272, 342);
            offCtx.quadraticCurveTo(268, 375, 285, 410);
            offCtx.moveTo(222, 330);
            offCtx.quadraticCurveTo(212, 375, 195, 415);
            // Hair & messy bun
            offCtx.moveTo(275, 235);
            offCtx.bezierCurveTo(240, 238, 218, 275, 225, 325);
            offCtx.bezierCurveTo(232, 365, 265, 385, 305, 375);
            // Hair waves
            offCtx.moveTo(255, 255);
            offCtx.bezierCurveTo(235, 285, 242, 335, 278, 358);
            // Romantic hair bun at the back
            offCtx.moveTo(312, 345);
            offCtx.bezierCurveTo(348, 335, 368, 368, 342, 392);
            offCtx.bezierCurveTo(322, 408, 298, 392, 305, 375);
            offCtx.stroke();

            // --- FLOATING LITTLE HEART BESIDE THEM ---
            offCtx.beginPath();
            const hx = 352, hy = 212, hs = 14;
            offCtx.moveTo(hx, hy + hs * 0.3);
            offCtx.bezierCurveTo(hx, hy - hs * 0.4, hx - hs, hy - hs * 0.4, hx - hs, hy + hs * 0.25);
            offCtx.bezierCurveTo(hx - hs, hy + hs * 0.85, hx, hy + hs * 1.25, hx, hy + hs * 1.5);
            offCtx.bezierCurveTo(hx, hy + hs * 1.25, hx + hs, hy + hs * 0.85, hx + hs, hy + hs * 0.25);
            offCtx.bezierCurveTo(hx + hs, hy - hs * 0.4, hx, hy - hs * 0.4, hx, hy + hs * 0.3);
            offCtx.stroke();

            const imgData = offCtx.getImageData(0, 0, size, size).data;
            const points = [];
            const step = 3; // Density of particles

            const scale = Math.min(width * 0.88, height * 0.68) / size;
            const offsetX = (width - size * scale) / 2;
            const offsetY = (height - size * scale) / 2 + height * 0.04;

            for (let y = 0; y < size; y += step) {
                for (let x = 0; x < size; x += step) {
                    const alpha = imgData[(y * size + x) * 4 + 3];
                    if (alpha > 128) {
                        points.push({
                            tx: offsetX + x * scale + (Math.random() - 0.5) * 2.5,
                            ty: offsetY + y * scale + (Math.random() - 0.5) * 2.5
                        });
                    }
                }
            }
            return points;
        }

        function buildTargets(instant = false) {
            const targets = getCoupleCoordinates();
            // Shuffle targets so particles fall organically across the whole silhouette
            targets.sort(() => Math.random() - 0.5);

            particles = targets.map((pt, i) => {
                const existing = particles[i];
                const delay = (i / targets.length) * 140; // Staggered falling frames
                return {
                    x: instant && existing ? pt.tx : Math.random() * width,
                    y: instant && existing ? pt.ty : -20 - Math.random() * height * 0.8,
                    tx: pt.tx,
                    ty: pt.ty,
                    vx: (Math.random() - 0.5) * 2,
                    vy: Math.random() * 2 + 1.5,
                    size: Math.random() * 1.8 + 1.1,
                    color: COLORS[Math.floor(Math.random() * COLORS.length)],
                    delay: instant ? 0 : delay,
                    arrived: instant,
                    twinkleOffset: Math.random() * Math.PI * 2,
                    isSparkle: Math.random() < 0.14
                };
            });
        }

        function typeWriter(text, el, speed = 75) {
            let i = 0;
            el.innerHTML = "";
            function type() {
                if (i < text.length) {
                    el.innerHTML += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                } else {
                    bottomHint.textContent = SUB_MESSAGE;
                    bottomHint.classList.add('visible');
                }
            }
            type();
        }

        function drawSparkleStar(x, y, r, color, alpha) {
            ctx.save();
            ctx.globalAlpha = alpha;
            ctx.strokeStyle = color;
            ctx.lineWidth = 1.1;
            ctx.beginPath();
            ctx.moveTo(x - r * 2.2, y);
            ctx.lineTo(x + r * 2.2, y);
            ctx.moveTo(x, y - r * 2.2);
            ctx.lineTo(x, y + r * 2.2);
            ctx.stroke();
            ctx.restore();
        }

        function spawnTouchMagic(x, y) {
            // Burst of glowing particles
            for (let i = 0; i < 24; i++) {
                const angle = Math.random() * Math.PI * 2;
                const speed = Math.random() * 4.5 + 1;
                touchBursts.push({
                    x,
                    y,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed - 1,
                    life: 1,
                    decay: Math.random() * 0.02 + 0.015,
                    color: COLORS[Math.floor(Math.random() * COLORS.length)],
                    size: Math.random() * 2.5 + 1
                });
            }
            // Cute floating mini heart
            floatingHearts.push({
                x,
                y,
                vy: -1.4 - Math.random(),
                vx: (Math.random() - 0.5) * 1.2,
                life: 1,
                scale: Math.random() * 0.5 + 0.7
            });
        }

        function drawMiniHeart(x, y, size, alpha) {
            ctx.save();
            ctx.globalAlpha = alpha;
            ctx.fillStyle = '#ff85b3';
            ctx.shadowColor = '#ff4d94';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            ctx.moveTo(x, y);
            ctx.bezierCurveTo(x, y - size / 2, x - size, y - size / 2, x - size, y + size / 4);
            ctx.bezierCurveTo(x - size, y + size, x, y + size * 1.3, x, y + size * 1.6);
            ctx.bezierCurveTo(x, y + size * 1.3, x + size, y + size, x + size, y + size / 4);
            ctx.bezierCurveTo(x + size, y - size / 2, x, y - size / 2, x, y);
            ctx.fill();
            ctx.restore();
        }

        let frame = 0;
        function animate() {
            frame++;
            // Soft trailing dark background
            ctx.fillStyle = 'rgba(8, 5, 15, 0.28)';
            ctx.fillRect(0, 0, width, height);

            // Draw twinkling background stars
            bgStars.forEach(s => {
                s.alpha += s.speed;
                const a = 0.25 + Math.abs(Math.sin(s.alpha)) * 0.65;
                ctx.fillStyle = `rgba(255, 240, 250, ${a})`;
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
                ctx.fill();
            });

            if (started) {
                let arrivedCount = 0;

                particles.forEach(p => {
                    if (p.delay > 0) {
                        p.delay--;
                        return;
                    }

                    const dx = p.tx - p.x;
                    const dy = p.ty - p.y;
                    const dist = Math.sqrt(dx * dx + dy * dy);

                    if (dist < 1.8) {
                        p.arrived = true;
                        arrivedCount++;
                        // Gentle breathing shimmer once settled
                        p.x = p.tx + Math.sin(frame * 0.04 + p.twinkleOffset) * 0.65;
                        p.y = p.ty + Math.cos(frame * 0.04 + p.twinkleOffset) * 0.65;
                    } else {
                        // Graceful falling & magnetic pull toward silhouette target
                        p.vx = p.vx * 0.9 + dx * 0.042;
                        p.vy = p.vy * 0.9 + dy * 0.042 + 0.15;
                        p.x += p.vx;
                        p.y += p.vy;
                    }

                    const twinkle = 0.65 + Math.sin(frame * 0.08 + p.twinkleOffset) * 0.35;
                    ctx.fillStyle = p.color;
                    ctx.globalAlpha = twinkle;
                    ctx.beginPath();
                    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                    ctx.fill();

                    if (p.isSparkle && twinkle > 0.92) {
                        drawSparkleStar(p.x, p.y, p.size * 1.4, '#ffffff', twinkle);
                    }
                    ctx.globalAlpha = 1;
                });

                // Trigger quote once 75% of particles have formed the couple
                if (!quoteStarted && particles.length > 0 && arrivedCount > particles.length * 0.75) {
                    quoteStarted = true;
                    typeWriter(ROMANTIC_QUOTE, quoteEl, 80);
                }
            }

            // Interactive touch bursts
            for (let i = touchBursts.length - 1; i >= 0; i--) {
                const b = touchBursts[i];
                b.x += b.vx;
                b.y += b.vy;
                b.vy += 0.06; // subtle gravity
                b.life -= b.decay;
                if (b.life <= 0) {
                    touchBursts.splice(i, 1);
                    continue;
                }
                ctx.globalAlpha = b.life;
                ctx.fillStyle = b.color;
                ctx.beginPath();
                ctx.arc(b.x, b.y, b.size, 0, Math.PI * 2);
                ctx.fill();
                ctx.globalAlpha = 1;
            }

            // Interactive floating hearts
            for (let i = floatingHearts.length - 1; i >= 0; i--) {
                const h = floatingHearts[i];
                h.x += h.vx;
                h.y += h.vy;
                h.life -= 0.012;
                if (h.life <= 0) {
                    floatingHearts.splice(i, 1);
                    continue;
                }
                drawMiniHeart(h.x, h.y, 8 * h.scale, h.life);
            }

            requestAnimationFrame(animate);
        }

        // Start experience on first tap/click
        function startExperience(e) {
            if (!started) {
                started = true;
                overlay.classList.add('hidden');
                playRomanticChime();
                buildTargets(false);
            }
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            if (clientX && clientY) spawnTouchMagic(clientX, clientY);
        }

        overlay.addEventListener('click', startExperience);
        overlay.addEventListener('touchstart', startExperience, { passive: true });

        canvas.addEventListener('click', (e) => {
            if (started) spawnTouchMagic(e.clientX, e.clientY);
        });
        canvas.addEventListener('touchmove', (e) => {
            if (started && Math.random() < 0.35) {
                spawnTouchMagic(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        animate();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=False)
