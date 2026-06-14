import { useState, useEffect } from "react";
import { MatrixRain } from "./MatrixRain/MatrixRain";
import type { AnimationPattern } from "../../types/animation";

export function Hero() {
  const [pattern, setPattern] = useState<AnimationPattern | null>(null);

  useEffect(() => {
    import("./MatrixRain/patterns/matrix").then((module) => {
      setPattern(module.default);
    });
  }, []);

  return (
    <section className="hero-overlay">
      {pattern && <MatrixRain pattern={pattern} />}
      
      <div className="relative z-10 text-center px-4">
        <h1 className="text-5xl md:text-7xl font-bold mb-6 text-white">
          Nolan Hofstee
        </h1>
        <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-2xl mx-auto">
          Software Engineer
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="#projects"
            className="px-8 py-3 bg-green-500/20 border border-green-500/50 rounded-lg text-green-400 hover:bg-green-500/30 transition-colors"
          >
            View Projects
          </a>
          <a
            href="#contact"
            className="px-8 py-3 border border-gray-600 rounded-lg text-gray-300 hover:border-gray-400 transition-colors"
          >
            Get in Touch
          </a>
        </div>
      </div>

      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <svg
          className="w-6 h-6 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 14l-7 7m0 0l-7-7m7 7V3"
          />
        </svg>
      </div>
    </section>
  );
}
