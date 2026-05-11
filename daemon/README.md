# Python Daemon

The core telemetry processing server.

## Setup

```bash
cd daemon
pip install -e .
```

## Usage

### Start the Daemon

```bash
python3 -m sc_telemetry.cli daemon start
```

The daemon will:
1. Listen for D-BOX packets on UDP 127.0.0.1:33740
2. Parse and normalize the telemetry
3. Broadcast standardized JSON on UDP 127.0.0.1:5555
4. Accept TCP connections on localhost:5050

### Custom Ports

```bash
python3 -m sc_telemetry.cli daemon start --port 5051  # Change TCP port
python3 -m sc_telemetry.cli daemon start --broadcast-port 5556  # Change UDP broadcast port
```

### Check Status

```bash
python3 -m sc_telemetry.cli daemon status
```

### Stop the Daemon

```bash
python3 -m sc_telemetry.cli daemon stop
```

## Modules

- **`parser.py`** - Decodes D-BOX binary packets
- **`normalizer.py`** - Converts parsed data to standard JSON format
- **`impact_detector.py`** - Detects and flags collision/impact events
- **`server.py`** - Main daemon server (UDP listener, TCP server, broadcaster)
- **`cli.py`** - Command-line interface

## Output Format

The daemon broadcasts JSON like:

```json
{
  "timestamp": 1234567890.123,
  "gforce": {
    "x": 0.5,
    "y": -0.2,
    "z": 1.1
  },
  "orientation": {
    "roll": 5.2,
    "pitch": -3.1,
    "heave": 0.8
  },
  "impact": {
    "detected": false,
    "magnitude": 0.0,
    "direction": null
  }
}
```
