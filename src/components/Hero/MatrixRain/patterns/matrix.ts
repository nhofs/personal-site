import type { AnimationPattern, MatrixColumn } from "../../../../types/animation";

const MATRIX_CHARS = "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF";
const FONT_SIZE = 14;

let cachedColumns: MatrixColumn[] | null = null;
let cachedWidth = 0;

function initializeColumns(width: number, height: number): MatrixColumn[] {
  const columnCount = Math.floor(width / FONT_SIZE);
  return Array.from({ length: columnCount }, () => ({
    y: Math.random() * height,
    speed: 0.5 + Math.random() * 1.5,
    characters: [],
  }));
}

function getRandomCharacter(): string {
  const randomIndex = Math.floor(Math.random() * MATRIX_CHARS.length);
  return MATRIX_CHARS[randomIndex] ?? "";
}

function renderColumn(
  context: CanvasRenderingContext2D,
  column: MatrixColumn,
  xPos: number,
  height: number,
  time: number
): void {
  const tailLength = 15 + Math.floor(Math.random() * 10);
  const flickerOffset = Math.sin(time * 0.001 + xPos) * 0.1;

  for (let position = 0; position < tailLength; position++) {
    const characterY = column.y - position * FONT_SIZE;
    if (characterY < 0 || characterY > height) continue;

    const fadeRatio = 1 - position / tailLength;
    const greenIntensity = Math.floor(255 * fadeRatio);
    const alpha = (fadeRatio + flickerOffset) * 0.8;

    if (position === 0) {
      context.fillStyle = `rgba(255, 255, 255, ${alpha})`;
    } else {
      context.fillStyle = `rgba(0, ${greenIntensity}, ${Math.floor(greenIntensity * 0.25)}, ${alpha})`;
    }

    const character = getRandomCharacter();
    context.fillText(character, xPos, characterY);
  }

  column.y += column.speed * 2;
  if (column.y > height + tailLength * FONT_SIZE) {
    column.y = -tailLength * FONT_SIZE;
    column.speed = 0.5 + Math.random() * 1.5;
  }
}

const matrixRainPattern: AnimationPattern = {
  name: "matrix",
  description: "Falling green characters from The Matrix",
  render: (context, width, height, time) => {
    if (!cachedColumns || cachedWidth !== width) {
      cachedColumns = initializeColumns(width, height);
      cachedWidth = width;
    }

    context.font = `${FONT_SIZE}px monospace`;

    cachedColumns.forEach((column, index) => {
      const xPos = index * FONT_SIZE;
      renderColumn(context, column, xPos, height, time);
    });
  },
};

export default matrixRainPattern;
