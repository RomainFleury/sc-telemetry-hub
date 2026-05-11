export interface Telemetry {
  timestamp: number;
  gforce: {
    x: number;
    y: number;
    z: number;
  };
  orientation: {
    roll: number;
    pitch: number;
    heave: number;
  };
  impact: {
    detected: boolean;
    magnitude: number;
    direction: {
      x: number;
      y: number;
      z: number;
    } | null;
  };
}

export interface LogEntry {
  message: string;
  level: 'info' | 'warning' | 'error' | 'debug';
  timestamp: string;
}
