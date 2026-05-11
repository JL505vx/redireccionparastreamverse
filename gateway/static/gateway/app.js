const canvas = document.getElementById('particles');
const ctx = canvas.getContext('2d');
let particles = [];

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const total = Math.min(95, Math.floor((canvas.width * canvas.height) / 15000));
    particles = Array.from({ length: total }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        r: Math.random() * 1.8 + 0.6,
        dx: (Math.random() - 0.5) * 0.28,
        dy: (Math.random() - 0.5) * 0.28,
        a: Math.random() * 0.55 + 0.18,
    }));
}

function drawParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach((particle) => {
        particle.x += particle.dx;
        particle.y += particle.dy;

        if (particle.x < 0 || particle.x > canvas.width) particle.dx *= -1;
        if (particle.y < 0 || particle.y > canvas.height) particle.dy *= -1;

        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(125, 211, 252, ${particle.a})`;
        ctx.fill();
    });

    for (let i = 0; i < particles.length; i += 1) {
        for (let j = i + 1; j < particles.length; j += 1) {
            const a = particles[i];
            const b = particles[j];
            const distance = Math.hypot(a.x - b.x, a.y - b.y);
            if (distance < 115) {
                ctx.strokeStyle = `rgba(148, 163, 184, ${0.14 * (1 - distance / 115)})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);
                ctx.stroke();
            }
        }
    }

    requestAnimationFrame(drawParticles);
}

function revealOnScroll() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, { threshold: 0.16 });

    document.querySelectorAll('.reveal').forEach((element) => observer.observe(element));
}

function startRedirectCountdown(targetUrl) {
    const counter = document.getElementById('countdown');
    let seconds = 3;

    const timer = setInterval(() => {
        seconds -= 1;
        counter.textContent = String(seconds);
        if (seconds <= 0) {
            clearInterval(timer);
            window.location.href = targetUrl;
        }
    }, 1000);
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();
drawParticles();
revealOnScroll();
