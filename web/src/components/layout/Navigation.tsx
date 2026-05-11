import { useLocation } from "react-router-dom";

export function Navigation() {
  const location = useLocation();

  const getTitle = () => {
    switch (location.pathname) {
      case "/telemetry":
        return "Live Telemetry";
      default:
        return "Star Citizen Telemetry Hub";
    }
  };

  return (
    <nav className="bg-slate-900/50 border-b border-slate-800 px-4 md:px-6 py-4 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center">
            <span className="text-xs font-bold">SC</span>
          </div>
          <h1 className="text-lg md:text-xl font-semibold">{getTitle()}</h1>
        </div>
      </div>
    </nav>
  );
}
