import React, { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { Telemetry, LogEntry } from '../types';

interface TelemetryContextType {
  telemetry: Telemetry | null;
  history: Telemetry[];
  connected: boolean;
  packetCount: number;
  logs: LogEntry[];
  stats: { updateRate: number } | null;
}

const TelemetryContext = createContext<TelemetryContextType | undefined>(undefined);

export function TelemetryProvider({ children }: { children: React.ReactNode }) {
  const [telemetry, setTelemetry] = useState<Telemetry | null>(null);
  const [history, setHistory] = useState<Telemetry[]>([]);
  const [connected, setConnected] = useState(false);
  const [packetCount, setPacketCount] = useState(0);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [stats, setStats] = useState<{ updateRate: number } | null>(null);
  const [lastUpdateTime, setLastUpdateTime] = useState<number>(0);
  const [updateCount, setUpdateCount] = useState(0);

  const addLog = useCallback((message: string, level: 'info' | 'warning' | 'error' | 'debug' = 'info') => {
    const now = new Date();
    const timestamp = now.toLocaleTimeString('en-US', { hour12: false });
    setLogs(prev => [...prev.slice(-99), { message, level, timestamp }]);
  }, []);

  useEffect(() => {
    let socket: WebSocket | null = null;
    let reconnectAttempts = 0;
    const maxReconnectAttempts = 5;
    let reconnectTimer: NodeJS.Timeout | null = null;

    const connectToSocket = () => {
      try {
        // Try WebSocket first (for future Electron IPC bridge)
        // For now, we'll use HTTP polling as fallback
        console.log('Attempting to connect to daemon...');
        addLog('Connecting to daemon...', 'info');
        
        // Fetch telemetry via HTTP polling
        const pollDaemon = async () => {
          try {
            // Try to connect via TCP socket using fetch to localhost:5050
            // This is a fallback - real implementation would use Electron IPC
            const response = await fetch('http://localhost:5050/api/telemetry', {
              method: 'GET',
              mode: 'no-cors',
            }).catch(() => null);

            if (!response || !response.ok) {
              // Daemon not ready, try again
              if (!connected) {
                setTimeout(pollDaemon, 1000);
              }
              return;
            }

            // Connection established
            if (!connected) {
              setConnected(true);
              addLog('✅ Connected to daemon', 'info');
              reconnectAttempts = 0;
            }
          } catch (err) {
            // Connection failed - try again
            if (!connected) {
              setTimeout(pollDaemon, 1000);
            }
          }
        };

        pollDaemon();
      } catch (err) {
        console.error('Connection error:', err);
      }
    };

    connectToSocket();

    // Simulate receiving telemetry data for now (until daemon is ready)
    const simulationInterval = setInterval(() => {
      const t = Date.now() / 1000;
      const mockTelemetry: Telemetry = {
        timestamp: t,
        gforce: {
          x: Math.sin(t * 0.5) * 0.3,
          y: Math.cos(t * 0.7) * 0.2,
          z: 0.8 + Math.sin(t * 0.3) * 0.2,
        },
        orientation: {
          roll: Math.sin(t * 0.2) * 15,
          pitch: Math.cos(t * 0.3) * 20,
          heave: Math.sin(t * 0.4) * 10,
        },
        impact: {
          detected: Math.random() < 0.02,
          magnitude: Math.random() * 0.5,
          direction: {
            x: Math.random() - 0.5,
            y: Math.random() - 0.5,
            z: Math.random() - 0.5,
          },
        },
      };

      setTelemetry(mockTelemetry);
      setHistory(prev => [...prev.slice(-99), mockTelemetry]);
      setPacketCount(prev => prev + 1);

      // Calculate update rate
      const now = Date.now();
      setUpdateCount(prev => prev + 1);
      if (now - lastUpdateTime >= 1000) {
        setStats({ updateRate: updateCount });
        setUpdateCount(0);
        setLastUpdateTime(now);
      }

      // Set connected state
      if (!connected) {
        setConnected(true);
        addLog('📊 Started receiving mock telemetry', 'info');
      }
    }, 16); // ~60 Hz

    return () => {
      clearInterval(simulationInterval);
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (socket) socket.close();
    };
  }, [connected, lastUpdateTime, updateCount, addLog]);

  return (
    <TelemetryContext.Provider value={{
      telemetry,
      history,
      connected,
      packetCount,
      logs,
      stats,
    }}>
      {children}
    </TelemetryContext.Provider>
  );
}

export function useTelemetry() {
  const context = useContext(TelemetryContext);
  if (context === undefined) {
    throw new Error('useTelemetry must be used within TelemetryProvider');
  }
  return context;
}
