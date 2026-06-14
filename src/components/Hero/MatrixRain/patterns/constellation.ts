import type { AnimationPattern } from "../../../../types/animation";

const PARTICLE_COUNT = 80;
const PARTICLE_SPEED = 0.3;
const CONNECTION_DISTANCE = 150;

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  hue: number;
}

let cachedParticles: Particle[] | null = null;

function createParticle(width: number, height: number): Particle {
  return {
    x: Math.random() * width,
    y: Math.random() * height,
    vx: (Math.random() - 0.5) * PARTICLE_SPEED,
    vy: (Math.random() - 0.5) * PARTICLE_SPEED,
    radius: Math.random() * 2 + 1,
    hue: Math.random() * 60 + 200,
  };
}

function initializeParticles(width: number, height: number): Particle[] {
  return Array.from({ length: PARTICLE_COUNT }, () => createParticle(width, height));
}

function updateParticle(particle: Particle, width: number, height: number): void {
  particle.x += particle.vx;
  particle.y += particle.vy;

  if (particle.x < 0 || particle.x > width) particle.vx *= -1;
  if (particle.y < 0 || particle.y > height) particle.vy *= -1;
}

function drawConnections(
  context: CanvasRenderingContext2D,
  particles: Particle[]
): void {
  for (let firstIndex = 0; firstIndex < particles.length; firstIndex++) {
    const first = particles[firstIndex];
    if (!first) continue;

    for (let secondIndex = firstIndex + 1; secondIndex < particles.length; secondIndex++) {
      const second = particles[secondIndex];
      if (!second) continue;

      const deltaX = first.x - second.x;
      const deltaY = first.y - second.y;
      const distance = Math.sqrt(deltaX * deltaX + deltaY * deltaY);

      if (distance < CONNECTION_DISTANCE) {
        const opacity = 1 - distance / CONNECTION_DISTANCE;
        context.strokeStyle = `hsla(220, 80%, 60%, ${opacity * 0.5})`;
        context.lineWidth = 0.5;
        context.beginPath();
        context.moveTo(first.x, first.y);
        context.lineTo(second.x, second.y);
        context.stroke();
      }
    }
  }
}

const constellationPattern: AnimationPattern = {
  name: "constellation",
  description: "Connected particles forming constellation patterns",
  render: (context, width, height, time) => {
    if (!cachedParticles) {
      cachedParticles = initializeParticles(width, height);
    }

    const pulseFactor = 0.8 + Math.sin(time * 0.002) * 0.2;

    cachedParticles.forEach((particle) => {
      updateParticle(particle, width, height);

      context.beginPath();
      context.arc(particle.x, particle.y, particle.radius * pulseFactor, 0, Math.PI * 2);
      context.fillStyle = `hsla(${particle.hue}, 80%, 60%, 0.8)`;
      context.fill();
    });

    drawConnections(context, cachedParticles);
  },
};

export default constellationPattern;
