# System Architecture

## Overview

The Star Citizen Telemetry Hub is a three-stage pipeline:

```
Star Citizen
    ↓
[UDP Port 33740]
    ↓
┌─────────────────────────────────┐
│   Stage 1: Ingress              │
│   - UDP listener                │
│   - Packet validation           │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│   Stage 2: Processing           │
│   - Binary parser               │
│   - Data normalization          │
│   - Impact detection            │
└─────────────┬───────────────────┘
              ↓
┌─────────────────────────────────┐
│   Stage 3: Egress               │
│   - UDP broadcast (5555)        │
│   - TCP socket (5050)           │
│   - Named pipes (Windows)       │
└─────────────────────────────────┘
              ↓
┌─────────────────────────────────┐
│   Consumers                     │
│   - 3rd Space Vest              │
│   - bHaptics Tactsuit           │
│   - SimHub                      │
│   - Custom apps                 │
└─────────────────────────────────┘
```

## Data Flow

### Input: Raw D-BOX Packet (UDP 33740)
Binary packet from Star Citizen containing:
- Header (validation)
- G-Force vectors (3 floats: X, Y, Z)
- Orientation (3 floats: roll, pitch, heave)
- Timestamp

### Processing

1. **Parser** (`parser.py`)
   - Validates packet header
   - Extracts binary values
   - Converts to float arrays

2. **Normalizer** (`normalizer.py`)
   - Scales values to standard range
   - Applies smoothing filter (optional)
   - Formats as JSON

3. **Impact Detector** (`impact_detector.py`)
   - Calculates G-Force magnitude
   - Detects sudden spikes
   - Flags collisions/impacts

### Output: Standardized JSON

```json
{
  "timestamp": 1234567890.123,
  "gforce": {"x": 0.5, "y": -0.2, "z": 1.1},
  "orientation": {"roll": 5.2, "pitch": -3.1, "heave": 0.8},
  "impact": {"detected": false, "magnitude": 0.0, "direction": null}
}
```

## Component Dependencies

```
Server (server.py)
  ├── Parser (parser.py)
  ├── Normalizer (normalizer.py)
  ├── Impact Detector (impact_detector.py)
  └── UDP/TCP Broadcaster

CLI (cli.py)
  └── Server

Electron UI (web/)
  └── TCP connection to Server:5050
```

## Network Topology

```
                    Star Citizen
                         │
                    [UDP 33740]
                         ↓
┌─────────────────────────────────┐
│   Telemetry Hub Daemon          │
│   (localhost:5050 TCP)          │
│   (localhost:5555 UDP broadcast)│
└──────┬──────────────┬───────────┘
       │              │
       │ TCP          │ UDP Broadcast
       │              │
   ┌───▼────┐    ┌────▼────────────────┐
   │Electron│    │External Consumers   │
   │  UI    │    │ - 3rd Space Vest    │
   └────────┘    │ - bHaptics          │
                 │ - SimHub            │
                 └─────────────────────┘
```

## Performance Characteristics

- **Latency**: <50ms (parsing + broadcasting)
- **Throughput**: 60-120 Hz (matches D-BOX stream)
- **Memory**: ~50 MB (Python daemon)
- **Packet Size**: ~100 bytes per update

## Error Handling

- Invalid packets: Logged, skipped (no downstream impact)
- Missing data fields: Filled with defaults (0.0)
- Connection loss: Automatic reconnect with exponential backoff
- Buffer overflow: Drops oldest packets, maintains real-time stream

## Extensibility

The modular design allows for:
- Custom parsers for other telemetry formats
- New impact detection algorithms
- Additional output channels (e.g., HTTP webhook)
- Plugin system for game-specific logic
