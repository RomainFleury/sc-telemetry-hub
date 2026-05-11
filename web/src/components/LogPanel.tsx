import { LogEntry } from "../types";

type Props = {
  logs: LogEntry[];
};

export function LogPanel({ logs }: Props) {
  return (
    <div className="space-y-1 text-xs font-mono">
      {logs.length === 0 ? (
        <div className="text-slate-500 italic">No logs yet...</div>
      ) : (
        logs.slice(-50).reverse().map((log, idx) => (
          <div
            key={idx}
            className={`py-1 px-2 rounded text-xs whitespace-pre-wrap break-words ${
              log.level === "error"
                ? "bg-red-900/20 text-red-300"
                : log.level === "warning"
                ? "bg-yellow-900/20 text-yellow-300"
                : log.level === "info"
                ? "bg-blue-900/20 text-blue-300"
                : "bg-slate-800/20 text-slate-300"
            }`}
          >
            <span className="text-slate-500">[{log.timestamp}]</span> {log.message}
          </div>
        ))
      )}
    </div>
  );
}
