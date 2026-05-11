import { Outlet } from "react-router-dom";
import { Sidebar } from "./Sidebar";
import { Navigation } from "./Navigation";
import { TelemetryProvider, useTelemetry } from "../../context/TelemetryContext";

function AppLayoutContent() {
  const { logs } = useTelemetry();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-slate-100">
      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar logs={logs} />

        {/* Main content area */}
        <div className="flex-1 flex flex-col overflow-hidden min-w-0">
          {/* Navigation */}
          <Navigation />

          {/* Page content */}
          <main className="flex-1 overflow-y-auto p-4 md:p-6">
            <Outlet />
          </main>
        </div>
      </div>
    </div>
  );
}

export function AppLayout() {
  return (
    <TelemetryProvider>
      <AppLayoutContent />
    </TelemetryProvider>
  );
}
