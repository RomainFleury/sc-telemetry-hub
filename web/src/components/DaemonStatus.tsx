import { useTelemetry } from "../context/TelemetryContext";

export function DaemonStatus() {
  const { connected, packetCount, stats } = useTelemetry();

  return (
    <div className="space-y-3">
      {/* Connection Status */}
      <div className="flex items-center justify-between p-3 rounded-lg bg-slate-800/50 border border-slate-700">
        <div className="flex items-center space-x-2">
          <div
            className={`w-2 h-2 rounded-full transition-colors ${
              connected ? "bg-green-500" : "bg-red-500"
            }`}
          />
          <span className="text-sm font-medium">
            {connected ? "Connected" : "Disconnected"}
          </span>
        </div>
      </div>

      {/* Stats */}
      {connected && stats && (
        <div className="space-y-2">
          <div className="p-2 rounded bg-slate-800/30 text-xs">
            <div className="text-slate-400">Packets Received</div>
            <div className="text-lg font-semibold text-cyan-400">{packetCount}</div>
          </div>
          <div className="p-2 rounded bg-slate-800/30 text-xs">
            <div className="text-slate-400">Update Rate</div>
            <div className="text-lg font-semibold text-cyan-400">{stats.updateRate.toFixed(1)} Hz</div>
          </div>
        </div>
      )}
    </div>
  );
}
