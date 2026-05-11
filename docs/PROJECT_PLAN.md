# Star Citizen Telemetry Hub - Project Plan

## Project Objective

Create a universal haptic telemetry bridge that intercepts Star Citizen's D-BOX telemetry stream (UDP port 33740) and makes it available to third-party hardware and software.

**Goal:** Unlock haptic feedback for VR vests (3rd Space Vest, bHaptics Tactsuit, OWO), racing wheels, SimHub, and custom integrations.

## Current Status

✅ **Complete:**
- Project repository setup (sc-telemetry-hub)
- README & documentation framework
- Architecture documentation (ARCHITECTURE.md)
- Example Python client (examples/python_client.py)
- CLI module (daemon/src/cli.py) - daemon start/stop/status/ping commands
- Server module (daemon/src/server.py) - UDP listener, TCP server, broadcaster
- Parser module (daemon/src/parser.py) - D-BOX packet parsing (placeholder)
- Normalizer module (daemon/src/normalizer.py) - Telemetry standardization
- Impact detector (daemon/src/impact_detector.py) - G-force spike detection

🚧 **In Progress:**
- Electron UI (web/) - React components for telemetry display
- TCP/WebSocket bridge for UI ↔ Daemon communication

❌ **Not Started:**
- D-BOX packet format documentation (reverse engineering needed)
- Windows batch scripts for easy setup
- Integration with 3rd Space Vest
- Integration with SimHub
- Comprehensive testing & validation

## Next Steps (Priority Order)

### Phase 1: Basic UI + Daemon Communication (Current)
**Goal:** Get the Electron UI running and displaying live telemetry from the daemon

**Tasks:**
1. ✅ Set up daemon core modules (parser, server, normalizer)
2. ⏳ Create Electron/React UI:
   - Main window with telemetry display (G-force, orientation)
   - Real-time graph for G-force over time
   - Impact detection log
   - Daemon status indicator
   - Log viewer (console output from daemon)
3. ⏳ Set up TCP socket bridge between UI and daemon
4. ⏳ Test with mock telemetry data (no D-BOX hardware needed)

**Definition of Done:**
- UI displays live telemetry updates every 100ms
- Daemon logs visible in UI console
- Can start/stop daemon from UI
- Works with mock data generator

### Phase 2: D-BOX Packet Format Discovery
**Goal:** Understand the actual D-BOX binary packet structure

**Tasks:**
1. Reverse engineer D-BOX packet format:
   - Sniff packets from Star Citizen
   - Document structure (header, fields, byte alignment)
   - Identify all telemetry fields
2. Update parser.py with correct implementation
3. Create packet format documentation (docs/PACKET_FORMAT.md)
4. Validate with real game data

**Definition of Done:**
- Parser correctly decodes real D-BOX packets
- Documentation reflects actual format
- Example packets included in docs

### Phase 3: Windows Setup & Distribution
**Goal:** Make it easy for SC community to install and run

**Tasks:**
1. Create Windows batch scripts:
   - windows/check-setup.bat - Verify Python/Node.js
   - windows/install-deps.bat - Install requirements
   - windows/start-daemon.bat - Start daemon
   - windows/start-ui.bat - Start UI
   - windows/start-all.bat - Start everything
2. Create windows/SETUP.md with step-by-step instructions
3. Test on Windows 10/11
4. Consider PyInstaller bundle for standalone executable

**Definition of Done:**
- Non-technical users can run `start-all.bat` and have everything working
- Clear error messages if dependencies missing

### Phase 4: Hardware Integration
**Goal:** Connect parsed telemetry to actual haptic hardware

**Tasks:**
1. **3rd Space Vest Integration:**
   - Use existing libthirdspacevest-simhub daemon
   - Create SimHub plugin bridge
   - Map G-force/impact data to vest feedback

2. **SimHub Direct Integration:**
   - Create SimHub plugin that connects to telemetry hub
   - Expose telemetry as custom data source
   - Allow custom mapping to existing effects

3. **Other Vests (bHaptics, OWO):**
   - Research APIs
   - Create adapter plugins

**Definition of Done:**
- 3rd Space Vest produces haptic feedback from SC telemetry
- SimHub shows telemetry data in plugin UI

## Architecture Summary

```
Star Citizen (D-BOX telemetry)
    ↓ UDP 33740
┌─────────────────────────────┐
│  Daemon (server.py)         │
│  - UDP listener (33740)     │
│  - Parser (parser.py)       │
│  - Normalizer (normalizer)  │
│  - Impact detector          │
│  - TCP server (5050)        │
│  - UDP broadcast (5555)     │
└─────────────────────────────┘
    ↓ TCP 5050 (JSON updates)
┌─────────────────────────────┐
│  Electron UI (web/)         │
│  - React components         │
│  - Telemetry display        │
│  - Daemon control           │
│  - Console/logs             │
└─────────────────────────────┘
    ↓ UDP 5555 (broadcast)
┌──────────────────────────────────────┐
│  External Consumers                  │
│  - 3rd Space Vest (SimHub bridge)    │
│  - Custom integrations               │
│  - Haptic rigs                       │
└──────────────────────────────────────┘
```

## File Structure

```
sc-telemetry-hub/
├── daemon/                       # Python daemon
│   ├── src/
│   │   ├── __init__.py
│   │   ├── cli.py               # ✅ CLI commands (start/stop/status)
│   │   ├── server.py            # ✅ Main server (UDP/TCP)
│   │   ├── parser.py            # ✅ D-BOX packet parser (placeholder)
│   │   ├── normalizer.py        # ✅ Data standardization
│   │   └── impact_detector.py   # ✅ Impact detection
│   ├── setup.py                 # ✅ Python package config
│   └── README.md                # ✅ Daemon docs
│
├── web/                          # Electron/React UI
│   ├── src/
│   │   ├── components/           # ⏳ React components
│   │   │   ├── TelemetryDisplay.tsx
│   │   │   ├── GForceGraph.tsx
│   │   │   ├── ImpactLog.tsx
│   │   │   └── DaemonStatus.tsx
│   │   ├── socket.ts             # ⏳ TCP socket client
│   │   └── App.tsx
│   ├── electron/                 # ⏳ Electron main process
│   ├── package.json              # ⏳ Node dependencies
│   └── README.md                 # ⏳ UI docs
│
├── windows/                      # ❌ Windows scripts (not started)
│   ├── check-setup.bat
│   ├── install-deps.bat
│   ├── start-all.bat
│   └── SETUP.md
│
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # ✅ System design
│   ├── PACKET_FORMAT.md          # ❌ D-BOX structure (needed)
│   ├── PROJECT_PLAN.md           # ✅ This file
│   └── INTEGRATION_GUIDE.md      # ❌ How to integrate (future)
│
├── examples/                     # Example integrations
│   ├── python_client.py          # ✅ UDP/TCP consumer
│   ├── nodejs_client.js          # ❌ Node consumer
│   └── csharp_client.cs          # ❌ C# consumer
│
├── README.md                     # ✅ Main overview
├── .gitignore                    # ✅ Ignore rules
└── LICENSE                       # ✅ MIT
```

## Key Decisions

1. **Python Daemon**: Easier D-BOX packet handling, simpler UDP/TCP server
2. **Electron UI**: Cross-platform, familiar tech stack (React)
3. **JSON Telemetry Format**: Universal, easy to parse, human-readable
4. **TCP + UDP Broadcast**: TCP for reliable UI updates, UDP for external apps
5. **Modular Parser**: Easy to update when real packet format is discovered

## Testing Strategy

1. **Unit Tests**: Parser, normalizer, impact detector
2. **Integration Tests**: Daemon ↔ UI communication
3. **System Tests**: Real D-BOX packets from Star Citizen
4. **User Tests**: Windows setup, end-user experience

## Known Issues & Blockers

1. **D-BOX Packet Format Unknown**: Parser is placeholder, needs reverse engineering
2. **No Test Hardware**: Can't test with real vest yet (community contribution)
3. **Electron Setup**: Need to scaffold React/Vite/Electron project

## How to Continue

### For Next Agent/Developer:

1. **Start with Phase 1 (UI):**
   ```bash
   cd web
   npm init vite . -- --template react
   npm install react-router-dom axios
   ```

2. **Create TCP socket client in web/src/socket.ts:**
   - Connect to localhost:5050
   - Listen for telemetry JSON
   - Emit events for React components

3. **Build React components:**
   - TelemetryDisplay: Show current G-force/orientation
   - GForceGraph: Plot G-force over time (use chart.js or recharts)
   - ImpactLog: Table of impact events
   - DaemonStatus: Connected/disconnected, packet count
   - Console: Display daemon logs

4. **Set up Electron main process:**
   - Spawn Python daemon on app start
   - Pass Python process output to renderer
   - Handle shutdown gracefully

5. **Test with mock data:**
   - Add `--mock` flag to daemon to generate fake telemetry
   - Verify UI updates correctly

### For D-BOX Format Discovery:

1. Run daemon in discover mode: `daemon/src/discover.py` (not yet created)
2. Sniff D-BOX packets from Star Citizen
3. Analyze hex patterns
4. Document in docs/PACKET_FORMAT.md
5. Update parser.py with correct structure

## References

- Original D-BOX announcement: https://robertsspaceindustries.com/spectrum/community/SC/forum/1/thread/wip-star-citizen-haptic-system-support-experimenta
- Related project: https://github.com/RomainFleury/libthirdspacevest-simhub
- D-BOX official: https://www.d-box.com/

## Contact & Questions

- Check existing issues/discussions on GitHub
- Reference ARCHITECTURE.md for system design details
- Check daemon/README.md for CLI usage
