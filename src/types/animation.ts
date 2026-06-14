export interface AnimationPattern {
  readonly name: string;
  readonly description: string;
  readonly render: (
    context: CanvasRenderingContext2D,
    width: number,
    height: number,
    time: number
  ) => void;
}

export interface CursorTrailPoint {
  readonly x: number;
  readonly y: number;
  readonly timestamp: number;
  readonly opacity: number;
}

export interface MatrixColumn {
  y: number;
  speed: number;
  characters: string[];
}
