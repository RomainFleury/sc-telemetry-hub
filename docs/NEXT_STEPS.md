# Immediate Next Steps

## What's Done ✅

1. **Daemon Core** - All modules exist but parser is placeholder
   - `daemon/src/cli.py` - Start/stop commands
   - `daemon/src/server.py` - UDP/TCP server
   - `daemon/src/parser.py` - Placeholder (needs real D-BOX format)
   - `daemon/src/normalizer.py` - JSON output
   - `daemon/src/impact_detector.py` - G-force spike detection

2. **Documentation**
   - README.md with overview
   - ARCHITECTURE.md with system design
   - Example Python client

## What's Next (Priority Order) 🚀

### 1. Set Up Electron/React UI (TODAY)

```bash
cd web
npm create vite . -- --template react
npm install
npm install axios react-router-dom
```

**What to build:**
- `src/App.tsx` - Main container
- `src/socket.ts` - TCP client (connect to daemon port 5050)
- `src/components/TelemetryDisplay.tsx` - Show current values
- `src/components/GForceGraph.tsx` - Real-time chart
- `src/components/ImpactLog.tsx` - Event log
- `src/components/DaemonStatus.tsx` - Status indicator
- `src/components/Console.tsx` - Daemon logs viewer
- `electron/main.ts` - Electron main process

### 2. Test Daemon + UI Communication (TODAY)

```bash
# Terminal 1: Start daemon with mock data
python3 -m sc_telemetry.cli daemon start --mock

# Terminal 2: Start UI
cd web && npm run dev
```

**Verify:**
- UI connects to daemon
- Real-time telemetry display updates
- No errors in console

### 3. Discover Real D-BOX Packet Format (ASAP)

**Create `daemon/src/discover.py`:**
```python
# Sniff UDP port 33740 and log hex packets
# Compare structure with parser expectations
# Document actual format
```

**Then update `daemon/src/parser.py` with correct binary format**

### 4. Windows Batch Scripts (THIS WEEK)

```batch
windows/
├── check-setup.bat      # Verify Python/Node installed
├── install-deps.bat     # pip install -e daemon && cd web && yarn
├── start-daemon.bat     # python3 -m sc_telemetry.cli daemon start
├── start-ui.bat         # cd web && yarn dev
├── start-all.bat        # Both in parallel
└── SETUP.md             # Instructions
```

## Code Template for TCP Socket Client

**`web/src/socket.ts`:**
```typescript
import { EventEmitter } from 'eventemitter3';

export class TelemetrySocket extends EventEmitter {
  private socket: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;

  connect(host: string = 'localhost', port: number = 5050) {
    // Create TCP connection to daemon
    // Listen for JSON telemetry updates
    // Emit 'telemetry' events
    // Handle disconnection and reconnection
  }

  disconnect() {
    // Clean shutdown
  }
}
```

## Mock Data Generator

**Add to `daemon/src/server.py`:**
```python
if '--mock' in sys.argv:
    # Generate fake telemetry instead of listening on UDP
    # Useful for testing without D-BOX hardware
    server.start_mock_data()
```

## Success Criteria

You'll know you're ready for Phase 2 when:
- ✅ Daemon starts without errors: `python3 -m sc_telemetry.cli daemon start`
- ✅ UI connects to daemon and receives telemetry
- ✅ G-force values update in real-time on UI
- ✅ Impact events logged and displayed
- ✅ Daemon logs visible in UI console
- ✅ Works with mock data (no D-BOX hardware needed)

## File to Edit First

**`daemon/setup.py`** - Make sure it has correct entry point:
```python
entry_points={
    'console_scripts': [
        'sc-telemetry=sc_telemetry.cli:main',
    ],
}
```

Then test:
```bash
cd daemon
pip install -e .
python3 -m sc_telemetry.cli --help
```

## Questions?

See:
- `docs/ARCHITECTURE.md` - System design
- `docs/PROJECT_PLAN.md` - Full roadmap
- `daemon/README.md` - Daemon CLI usage
- `README.md` - Project overview
