import { TelemetryDisplay } from "../components/TelemetryDisplay";

export function LiveTelemetryPage() {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Live Telemetry</h2>
        <p className="text-slate-400">Real-time D-BOX telemetry data from Star Citizen</p>
      </div>
      <TelemetryDisplay />
    </div>
  );
}
