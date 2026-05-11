import { Telemetry } from "../types";

type Props = {
  history: Telemetry[];
};

export function GForceGraph({ history }: Props) {
  if (history.length === 0) {
    return null;
  }

  // Calculate dimensions
  const width = 400;
  const height = 200;
  const padding = 40;
  const graphWidth = width - padding * 2;
  const graphHeight = height - padding * 2;

  // Find max magnitude for scaling
  const magnitudes = history.map(t => 
    Math.sqrt(t.gforce.x ** 2 + t.gforce.y ** 2 + t.gforce.z ** 2)
  );
  const maxMagnitude = Math.max(...magnitudes, 1);
  const scale = graphHeight / maxMagnitude;

  // Create path data
  const points = history.map((t, i) => {
    const magnitude = Math.sqrt(t.gforce.x ** 2 + t.gforce.y ** 2 + t.gforce.z ** 2);
    const x = padding + (i / (history.length - 1 || 1)) * graphWidth;
    const y = height - padding - magnitude * scale;
    return [x, y];
  });

  const pathData = points.map((p, i) => (i === 0 ? `M${p[0]},${p[1]}` : `L${p[0]},${p[1]}`)).join(' ');

  return (
    <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
      <div className="text-xs text-slate-400 mb-4">G-Force Magnitude (Last 100 samples)</div>
      <svg width={width} height={height} className="w-full border border-slate-700 rounded bg-slate-900/30">
        {/* Grid lines */}
        <line x1={padding} y1={height - padding} x2={width - padding} y2={height - padding} stroke="#475569" strokeWidth="1" />
        <line x1={padding} y1={padding} x2={padding} y2={height - padding} stroke="#475569" strokeWidth="1" />

        {/* Y-axis labels */}
        <text x="5" y={height - padding + 4} fontSize="10" fill="#94a3b8">0G</text>
        <text x="5" y={padding + 4} fontSize="10" fill="#94a3b8">{maxMagnitude.toFixed(1)}G</text>

        {/* Line graph */}
        <path
          d={pathData}
          fill="none"
          stroke="#06b6d4"
          strokeWidth="2"
          vectorEffect="non-scaling-stroke"
        />

        {/* Area under curve */}
        <path
          d={pathData + ` L${width - padding},${height - padding} L${padding},${height - padding} Z`}
          fill="url(#gradient)"
          opacity="0.2"
        />

        {/* Gradient definition */}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#06b6d4" />
            <stop offset="100%" stopColor="#06b6d4" stopOpacity="0" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
}
