# Immediate Next Steps

## What's Done ✅

1. **Daemon Core** - All modules exist but parser is placeholder
   - `daemon/setup.py` maps package **`sc_telemetry`** to the **`src/`** directory (`pip install -e .` from `daemon/`)
   - `daemon/src/cli.py` - Start/stop, `discover`, `test-parser`, `ping`
   - `daemon/src/server.py` - UDP/TCP server (newline-delimited JSON; `ping` / `shutdown` over TCP)
   - `daemon/src/parser.py` - Placeholder (needs real D-BOX format)
   - `daemon/src/normalizer.py` - JSON output
   - `daemon/src/impact_detector.py` - G-force spike detection

2. **Documentation**
   - README.md with overview
   - ARCHITECTURE.md with system design
   - Example Python client

## What's Next (Priority Order) 🚀

### 1. Wire the Electron/React UI to the daemon (TODAY)

The `web/` Vite + React + Electron scaffold is in place. Next work:

- Replace the placeholder `fetch('http://localhost:5050/api/telemetry')` path in `web/src/context/TelemetryContext.tsx` with a real TCP or Electron IPC bridge to the daemon (newline-delimited JSON on port **5050**, same as `examples/python_client.py` TCP mode).
- Optional: add `web/src/socket.ts` (or preload IPC) as a thin client over that stream.

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

Use the CLI (no separate script needed):

```bash
cd daemon && pip install -e .
python -m sc_telemetry.cli discover --port 33740
python -m sc_telemetry.cli test-parser "<paste hex from discover>"
```

Then update `daemon/src/parser.py` with the correct binary layout and document it under `docs/` when confirmed.

### 4. Windows Batch Scripts (THIS WEEK)

```batch
windows/
├── check-setup.bat          # Orchestrator (like libthirdspacevest-simhub)
├── install-deps.bat         # pip install -e daemon + yarn install web
├── start-daemon.bat         # sc_telemetry.cli daemon start
├── start-ui.bat             # yarn dev in web/
├── start-all.bat            # Daemon (new window) + UI
├── .env.bat.example         # Copy to .env.bat → set STH_PYTHON=...
├── README.md
├── SETUP.md
└── setup/
    ├── resolve-python.bat
    ├── check-python.bat
    ├── check-node.bat
    ├── check-yarn.bat
    ├── check-python-packages.bat
    └── check-web-dependencies.bat
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
