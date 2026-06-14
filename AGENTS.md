# AGENTS.md

## Project

Personal portfolio site — Vite + React + TypeScript, hosted on GitHub Pages.

## Commands

```bash
npm run dev          # Start dev server
npm run build        # Production build (output: dist/)
npm run preview      # Preview production build locally
npm run lint         # ESLint
```

No test framework configured yet.

## Architecture

- **Stack**: Vite 6, React 19, TypeScript (strict), Tailwind CSS v4
- **Entry**: `src/main.tsx` → `src/App.tsx`
- **Components**: `src/components/{Hero,About,Projects,Contact}/`
- **Cursor reveal**: `src/components/Hero/MatrixRain/` — swappable animation patterns
- **Pattern system**: Drop a new `AnimationPattern` implementation in `patterns/`, register it in `patterns/index.ts`

## Conventions

- **TypeScript**: `strict: true`, `noUncheckedIndexedAccess`. No `any`, no casts. Helper functions over monoliths. Variable names ≥ 3 chars.
- **Styling**: Tailwind utility classes. Custom CSS only in `src/index.css` for canvas/animation concerns.
- **Imports**: Relative within `src/`, no path aliases.
- **Component naming**: PascalCase files, named exports (no default exports for components).

## Patterns

To swap the reveal animation:
1. Create `src/components/Hero/MatrixRain/patterns/yourpattern.ts`
2. Export a default `AnimationPattern` object
3. Import and use in `Hero.tsx` instead of `matrix`

Available patterns: `matrix` (default), `constellation`

## Deploy

GitHub Pages from `dist/` on push to `main`. Custom domain: add `CNAME` file in `public/`.
