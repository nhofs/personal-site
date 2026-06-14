import { useEffect, useRef, useCallback } from "react";
import type { CursorTrailPoint, AnimationPattern } from "../../../types/animation";

interface MatrixRainProps {
  pattern: AnimationPattern;
  trailDuration?: number;
  revealRadius?: number;
}

export function MatrixRain({
  pattern,
  trailDuration = 2000,
  revealRadius = 150,
}: MatrixRainProps) {
  const backgroundCanvasRef = useRef<HTMLCanvasElement>(null);
  const revealCanvasRef = useRef<HTMLCanvasElement>(null);
  const trailPointsRef = useRef<CursorTrailPoint[]>([]);
  const animationFrameRef = useRef<number>(0);

  const handleMouseMove = useCallback(
    (event: MouseEvent) => {
      const newPoint: CursorTrailPoint = {
        x: event.clientX,
        y: event.clientY,
        timestamp: Date.now(),
        opacity: 1,
      };
      trailPointsRef.current.push(newPoint);
    },
    []
  );

  const handleTouchMove = useCallback(
    (event: TouchEvent) => {
      const touch = event.touches[0];
      if (!touch) return;

      const newPoint: CursorTrailPoint = {
        x: touch.clientX,
        y: touch.clientY,
        timestamp: Date.now(),
        opacity: 1,
      };
      trailPointsRef.current.push(newPoint);
    },
    []
  );

  const drawRevealMask = useCallback(
    (context: CanvasRenderingContext2D, width: number, height: number) => {
      const currentTime = Date.now();

      context.globalCompositeOperation = "source-over";
      const gradient = context.createLinearGradient(0, 0, 0, height);
      gradient.addColorStop(0, "#0f1729");
      gradient.addColorStop(1, "#000000");
      context.fillStyle = gradient;
      context.fillRect(0, 0, width, height);

      context.globalCompositeOperation = "destination-out";

      trailPointsRef.current = trailPointsRef.current.filter((point) => {
        const elapsed = currentTime - point.timestamp;
        return elapsed < trailDuration;
      });

      trailPointsRef.current.forEach((point) => {
        const elapsed = currentTime - point.timestamp;
        const lifeRatio = 1 - elapsed / trailDuration;
        const currentRadius = revealRadius * (0.5 + lifeRatio * 0.5);

        const gradient = context.createRadialGradient(
          point.x,
          point.y,
          0,
          point.x,
          point.y,
          currentRadius
        );
        gradient.addColorStop(0, `rgba(0, 0, 0, ${lifeRatio})`);
        gradient.addColorStop(0.7, `rgba(0, 0, 0, ${lifeRatio * 0.4})`);
        gradient.addColorStop(1, "rgba(0, 0, 0, 0)");

        context.beginPath();
        context.arc(point.x, point.y, currentRadius, 0, Math.PI * 2);
        context.fillStyle = gradient;
        context.fill();
      });

      context.globalCompositeOperation = "source-over";
    },
    [trailDuration, revealRadius]
  );

  useEffect(() => {
    const backgroundCanvas = backgroundCanvasRef.current;
    const revealCanvas = revealCanvasRef.current;

    if (!backgroundCanvas || !revealCanvas) return;

    const backgroundContext = backgroundCanvas.getContext("2d");
    const revealContext = revealCanvas.getContext("2d");

    if (!backgroundContext || !revealContext) return;

    const resizeCanvas = () => {
      const width = window.innerWidth;
      const height = window.innerHeight;

      backgroundCanvas.width = width;
      backgroundCanvas.height = height;
      revealCanvas.width = width;
      revealCanvas.height = height;
    };

    const renderFrame = (timestamp: number) => {
      const width = window.innerWidth;
      const height = window.innerHeight;

      backgroundContext.fillStyle = "rgba(10, 10, 10, 0.05)";
      backgroundContext.fillRect(0, 0, width, height);

      pattern.render(backgroundContext, width, height, timestamp);

      drawRevealMask(revealContext, width, height);

      animationFrameRef.current = requestAnimationFrame(renderFrame);
    };

    resizeCanvas();

    window.addEventListener("resize", resizeCanvas);
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("touchmove", handleTouchMove);

    animationFrameRef.current = requestAnimationFrame(renderFrame);

    return () => {
      window.removeEventListener("resize", resizeCanvas);
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("touchmove", handleTouchMove);
      cancelAnimationFrame(animationFrameRef.current);
    };
  }, [handleMouseMove, handleTouchMove, drawRevealMask, pattern]);

  return (
    <>
      <canvas
        ref={backgroundCanvasRef}
        className="matrix-canvas"
        aria-hidden="true"
      />
      <canvas
        ref={revealCanvasRef}
        className="reveal-mask"
        aria-hidden="true"
      />
    </>
  );
}
