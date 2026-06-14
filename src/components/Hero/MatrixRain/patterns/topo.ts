import type { AnimationPattern } from "../../../../types/animation";

const LINE_COUNT = 12;
const BASE_OPACITY = 0.15;

function noise(x: number, y: number, t: number): number {
  const a = Math.sin(x * 0.008 + t * 0.0003) * Math.cos(y * 0.006 + t * 0.0002);
  const b = Math.sin(x * 0.005 - t * 0.0004) * Math.cos(y * 0.009 - t * 0.0003);
  const c = Math.sin((x + y) * 0.004 + t * 0.0005);
  return (a + b + c) / 3;
}

function drawContourLine(
  context: CanvasRenderingContext2D,
  width: number,
  height: number,
  threshold: number,
  time: number,
  alpha: number
): void {
  const step = 6;
  context.beginPath();

  for (let y = 0; y < height; y += step) {
    for (let x = 0; x < width; x += step) {
      const value = noise(x, y, time);
      const nextX = noise(x + step, y, time);
      const nextY = noise(x, y + step, time);

      if ((value < threshold && nextX >= threshold) || (value >= threshold && nextX < threshold)) {
        const t = (threshold - value) / (nextX - value);
        const ix = x + t * step;
        context.moveTo(ix, y);
        context.lineTo(ix + 0.5, y + step);
      }

      if ((value < threshold && nextY >= threshold) || (value >= threshold && nextY < threshold)) {
        const t = (threshold - value) / (nextY - value);
        const iy = y + t * step;
        context.moveTo(x, iy);
        context.lineTo(x + step, iy + 0.5);
      }
    }
  }

  context.strokeStyle = `rgba(100, 160, 220, ${alpha})`;
  context.lineWidth = 1;
  context.stroke();
}

const topoPattern: AnimationPattern = {
  name: "topo",
  description: "Animated topographic contour lines",
  render: (context, width, height, time) => {
    for (let i = 0; i < LINE_COUNT; i++) {
      const threshold = (i / LINE_COUNT) * 2 - 1;
      const pulse = Math.sin(time * 0.001 + i * 0.5) * 0.03;
      const alpha = BASE_OPACITY + pulse;
      drawContourLine(context, width, height, threshold, time, alpha);
    }
  },
};

export default topoPattern;
