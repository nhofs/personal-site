import { useState, useEffect } from "react";
import { MatrixRain } from "./MatrixRain/MatrixRain";
import type { AnimationPattern } from "../../types/animation";

export function Hero() {
  const [pattern, setPattern] = useState<AnimationPattern | null>(null);

  useEffect(() => {
    import("./MatrixRain/patterns/topo").then((module) => {
      setPattern(module.default);
    });
  }, []);

  return (
    <section className="hero-overlay">
      {pattern && <MatrixRain pattern={pattern} />}
      
      <div className="relative z-10 text-center w-full px-4">
        <h1 className="text-7xl md:text-9xl lg:text-[10rem] font-bold mb-6 text-white tracking-tight drop-shadow-[0_0_40px_rgba(255,255,255,0.1)]">
          Nolan Hofstee
        </h1>
        <p className="text-2xl md:text-4xl text-gray-400 mb-24 font-light tracking-wide">
          Software Engineer
        </p>
        <div className="flex flex-col items-center gap-6">
          <div className="flex flex-col sm:flex-row gap-6 justify-center items-center">
            <a
              href="#projects"
              style={{ padding: "28px 56px" }}
              className="text-center bg-green-500/15 border-2 border-green-500/40 rounded-2xl text-green-400 text-xl font-semibold hover:bg-green-500/25 hover:border-green-500/60 hover:shadow-[0_0_40px_rgba(0,255,65,0.2)] transition-all duration-300"
            >
              View Projects
            </a>
            <a
              href="#about"
              style={{ padding: "28px 56px" }}
              className="text-center bg-green-500/15 border-2 border-green-500/40 rounded-2xl text-green-400 text-xl font-semibold hover:bg-green-500/25 hover:border-green-500/60 hover:shadow-[0_0_40px_rgba(0,255,65,0.2)] transition-all duration-300"
            >
              About Me
            </a>
          </div>
          <a
            href="#contact"
            style={{ padding: "28px 56px" }}
            className="text-center border-2 border-gray-600 rounded-2xl text-gray-300 text-xl font-semibold hover:border-gray-400 hover:text-white hover:shadow-[0_0_40px_rgba(255,255,255,0.08)] transition-all duration-300"
          >
            Contact Me
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
