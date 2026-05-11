# Star Citizen Telemetry Hub

A universal haptic telemetry bridge for Star Citizen's D-BOX integration, enabling third-party hardware and software to hook into the D-BOX telemetry stream.

## Overview

Star Citizen's official [D-BOX haptic support](https://robertsspaceindustries.com/spectrum/community/SC/forum/1/thread/wip-star-citizen-haptic-system-support-experimenta) provides high-frequency telemetry data (via UDP on port 33740) that was previously limited to D-BOX hardware. **Telemetry Hub** intercepts and standardizes this stream, making it available to any external application through multiple interfaces.

### Why This Matters

The D-BOX telemetry stream contains rich, real-time data:
- **G-Force vectors** (X, Y, Z axes)
- **Orientation data** (roll, pitch, heave)
- **Impact detection** (directional hits, collisions)
- **High frequency updates** (~60-120 Hz)

Currently, this data is locked to D-BOX hardware. Telemetry Hub unlocks it for:
- VR haptic vests (3rd Space Vest, bHaptics Tactsuit, OWO, etc.)
- Racing wheels and pedals
- Custom haptic rigs
- SimHub integrations
- Research and telemetry analysis

## Architecture

The project follows a **Python daemon + Electron UI** pattern (similar to [libthirdspacevest-simhub](https://github.com/RomainFleury/libthirdspacevest-simhub)):

| Layer | Technology | Function |
|---|---|---|
| **Ingress** | UDP Socket (port 33740) | Captures raw D-BOX binary packets from Star Citizen |
| **Parser** | Python | Decodes binary telemetry into structured data (G-force, orientation) |
| **Logic** | Python Daemon | Normalizes data, detects impacts, broadcasts to external apps |
| **Egress** | UDP Broadcast, JSON | Re-sends standardized telemetry on public port (e.g., 5555) |
| **UI** | Electron + React | Real-time telemetry monitor & daemon controls |

## Project Structure

```
sc-telemetry-hub/
├── daemon/                          # Python daemon (telemetry server)
│   ├── src/
│   │   ├── __init__.py
│   │   ├── cli.py                   # Command-line interface
│   │   ├── server.py                # Main daemon server
│   │   ├── parser.py                # D-BOX packet parser
│   │   ├── normalizer.py            # Telemetry standardization
│   │   └── impact_detector.py       # Impact/spike detection
│   ├── setup.py
│   └── README.md
├── web/                             # Electron + React UI
│   ├── src/
│   ├── electron/
│   ├── package.json
│   └── README.md
├── docs/                            # Documentation & research
│   ├── ARCHITECTURE.md              # Detailed design docs
│   ├── PACKET_FORMAT.md             # D-BOX packet structure
│   └── INTEGRATION_GUIDE.md         # How to connect external apps
├── examples/                        # Example clients & integrations
│   ├── python_client.py
│   ├── nodejs_client.js
│   └── csharp_client.cs
├── .gitignore
├── LICENSE
└── README.md (this file)
```

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (LTS)
- Yarn or npm

### macOS / Linux

```bash
# 1. Install Python daemon
cd daemon && pip install -e . && cd ..

# 2. Start the daemon
python3 -m sc_telemetry.cli daemon start

# 3. In another terminal, start the UI
cd web && yarn install && yarn dev
```

### Windows

```batch
# 1. Install Node.js LTS and Python 3.10+
# 2. Double-click windows/check-setup.bat (checks prerequisites)
# 3. Double-click windows/start-all.bat
```

## How It Works

### Phase 1: Interception
- Telemetry Hub listens on UDP port 33740 (D-BOX default)
- Captures raw binary packets from Star Citizen
- Validates packet headers to ensure authenticity

### Phase 2: Standardization
- Parses binary data into float values:
  - G-Force X, Y, Z
  - Roll, Pitch, Heave
  - Impact magnitude & direction
- Outputs clean JSON format

### Phase 3: Broadcasting
External apps can consume the telemetry via:
- **UDP Broadcast** (port 5555): Fire-and-forget, low latency
- **TCP Socket** (port 5050): Reliable connection, multiple clients
- **Named Pipes** (Windows only): Ultra-low latency for local apps

## Example Usage

### Python Client
```python
import json
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("127.0.0.1", 5555))

while True:
    data, addr = sock.recvfrom(1024)
    telemetry = json.loads(data.decode())
    print(f"G-Force: {telemetry['gforce_x']:.2f}G")
```

### JavaScript/Node.js Client
```javascript
const dgram = require('dgram');
const client = dgram.createSocket('udp4');

client.on('message', (msg, rinfo) => {
    const telemetry = JSON.parse(msg.toString());
    console.log(`Pitch: ${telemetry.pitch.toFixed(2)}°`);
});

client.bind(5555);
```

## Development

### Running the Discovery Tool

To see raw D-BOX packets from Star Citizen:

```bash
python3 -m sc_telemetry.cli discover --port 33740
```

This logs hex dumps of all packets to help you understand the packet structure.

### Testing the Parser

```bash
python3 -m sc_telemetry.cli test-parser --packet <hex_data>
```

### Daemon Commands

```bash
python3 -m sc_telemetry.cli daemon start              # Start on default port 5050
python3 -m sc_telemetry.cli daemon start --port 5051  # Custom port
python3 -m sc_telemetry.cli daemon status             # Check if running
python3 -m sc_telemetry.cli daemon stop               # Stop the daemon
```

## Configuration

Create a `.env` file in the project root:

```env
# D-BOX input (Star Citizen sends here)
DBOX_INPUT_PORT=33740
DBOX_INPUT_HOST=127.0.0.1

# Telemetry Hub outputs
DAEMON_PORT=5050
BROADCAST_PORT=5555

# Impact detection sensitivity (0.0 to 1.0)
IMPACT_THRESHOLD=0.3

# Telemetry buffer size (milliseconds)
BUFFER_MS=50
```

## Documentation

- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - System design & data flow
- **[PACKET_FORMAT.md](./docs/PACKET_FORMAT.md)** - D-BOX packet structure & field definitions
- **[INTEGRATION_GUIDE.md](./docs/INTEGRATION_GUIDE.md)** - How to connect external hardware/software
- **[daemon/README.md](./daemon/README.md)** - Python daemon documentation
- **[web/README.md](./web/README.md)** - Electron UI documentation

## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

[MIT License](./LICENSE)

## Related Projects

- **[libthirdspacevest-simhub](https://github.com/RomainFleury/libthirdspacevest-simhub)** - Third Space Vest driver & debugger
- **[D-BOX HaptiSync](https://www.d-box.com/)** - Official D-BOX hardware & software
- **[Star Citizen](https://robertsspaceindustries.com/)** - The game that started it all

## Support

- 🐛 [Report bugs](https://github.com/RomainFleury/sc-telemetry-hub/issues)
- 💬 [Discussions](https://github.com/RomainFleury/sc-telemetry-hub/discussions)
- 📖 [Documentation](./docs/)

---

**Disclaimer:** This project is unofficial and not affiliated with Cloud Imperium Games or D-BOX Technologies. It is a community effort to unlock the potential of Star Citizen's haptic telemetry stream.