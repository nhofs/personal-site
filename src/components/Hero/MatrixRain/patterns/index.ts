import type { AnimationPattern } from "../../../../types/animation";

export const patterns = {
  matrix: () => import("./matrix"),
  constellation: () => import("./constellation"),
  topo: () => import("./topo"),
} as const;

export type PatternName = keyof typeof patterns;

export async function loadPattern(name: PatternName): Promise<AnimationPattern> {
  const module = await patterns[name]();
  return module.default;
}
