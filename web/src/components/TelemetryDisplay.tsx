import { useTelemetry } from "../context/TelemetryContext";
import { GForceGraph } from "./GForceGraph";

export function TelemetryDisplay() {
  const { telemetry, history } = useTelemetry();

  if (!telemetry) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-400">Waiting for telemetry data...</p>
      </div>
    );
  }

  const magnitude = Math.sqrt(
    telemetry.gforce.x ** 2 +
    telemetry.gforce.y ** 2 +
    telemetry.gforce.z ** 2
  );

  return (
    <div className="space-y-6">
      {/* G-Force Current Values */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">G-Force X</div>
          <div className={`text-3xl font-bold ${
            Math.abs(telemetry.gforce.x) > 0.5 ? "text-orange-400" : "text-cyan-400"
          }`}>
            {telemetry.gforce.x.toFixed(2)}G
          </div>
        </div>
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">G-Force Y</div>
          <div className={`text-3xl font-bold ${
            Math.abs(telemetry.gforce.y) > 0.5 ? "text-orange-400" : "text-cyan-400"
          }`}>
            {telemetry.gforce.y.toFixed(2)}G
          </div>
        </div>
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">G-Force Z</div>
          <div className={`text-3xl font-bold ${
            Math.abs(telemetry.gforce.z) > 0.5 ? "text-orange-400" : "text-cyan-400"
          }`}>
            {telemetry.gforce.z.toFixed(2)}G
          </div>
        </div>
      </div>

      {/* Total Magnitude */}
      <div className="p-4 rounded-lg bg-gradient-to-r from-slate-800/50 to-slate-700/30 border border-slate-700">
        <div className="text-xs text-slate-400 mb-2">Total G-Force Magnitude</div>
        <div className={`text-4xl font-bold ${
          magnitude > 0.5 ? "text-orange-400" : "text-cyan-400"
        }`}>
          {magnitude.toFixed(2)}G
        </div>
      </div>

      {/* Orientation */}
      <div className="grid grid-cols-3 gap-4">
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">Roll</div>
          <div className="text-2xl font-bold text-purple-400">
            {telemetry.orientation.roll.toFixed(1)}°
          </div>
        </div>
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">Pitch</div>
          <div className="text-2xl font-bold text-purple-400">
            {telemetry.orientation.pitch.toFixed(1)}°
          </div>
        </div>
        <div className="p-4 rounded-lg bg-slate-800/50 border border-slate-700">
          <div className="text-xs text-slate-400 mb-2">Heave</div>
          <div className="text-2xl font-bold text-purple-400">
            {telemetry.orientation.heave.toFixed(1)}°
          </div>
        </div>
      </div>

      {/* Impact Detection */}
      {telemetry.impact.detected && (
        <div className="p-4 rounded-lg bg-red-900/20 border border-red-800 animate-pulse">
          <div className="text-xs text-red-400 mb-2">⚠️ IMPACT DETECTED</div>
          <div className="text-2xl font-bold text-red-400">
            {telemetry.impact.magnitude.toFixed(2)}G
          </div>
          {telemetry.impact.direction && (
            <div className="text-xs text-red-300 mt-2">
              Direction: X={telemetry.impact.direction.x.toFixed(2)}, Y={telemetry.impact.direction.y.toFixed(2)}, Z={telemetry.impact.direction.z.toFixed(2)}
            </div>
          )}
        </div>
      )}

      {/* G-Force Graph */}
      <GForceGraph history={history} />
    </div>
  );
}
