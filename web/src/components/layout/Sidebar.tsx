import { DaemonStatus } from "../DaemonStatus";
import { LogPanel } from "../LogPanel";
import { LogEntry } from "../../types";

type Props = {
  logs: LogEntry[];
};

export function Sidebar({ logs }: Props) {
  return (
    <aside className="w-80 md:w-96 bg-slate-900/50 border-r border-slate-800 flex flex-col shrink-0">
      {/* Daemon Status */}
      <div className="p-3 md:p-4 border-b border-slate-800 shrink-0">
        <DaemonStatus />
      </div>

      {/* Logs - Take remaining space */}
      <div className="flex-1 overflow-hidden flex flex-col p-3 md:p-4 min-h-0">
        <div className="text-xs font-semibold text-slate-400 mb-3">DAEMON LOGS</div>
        <div className="flex-1 overflow-y-auto">
          <LogPanel logs={logs} />
        </div>
      </div>
    </aside>
  );
}
