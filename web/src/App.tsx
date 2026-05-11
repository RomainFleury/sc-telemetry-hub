import { HashRouter, Routes, Route, Navigate } from "react-router-dom";
import { AppLayout } from "./components/layout/AppLayout";
import { LiveTelemetryPage } from "./pages/LiveTelemetryPage";

function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<AppLayout />}>
          <Route index element={<Navigate to="/telemetry" replace />} />
          <Route path="telemetry" element={<LiveTelemetryPage />} />
        </Route>
      </Routes>
    </HashRouter>
  );
}

export default App;
