#!/usr/bin/env python3
"""Example Python client consuming telemetry from Telemetry Hub."""

import json
import socket
import sys
from dataclasses import dataclass


@dataclass
class Telemetry:
    timestamp: float
    gforce_x: float
    gforce_y: float
    gforce_z: float
    roll: float
    pitch: float
    heave: float
    impact_detected: bool
    impact_magnitude: float


def udp_consumer(host="127.0.0.1", port=5555):
    """Listen for UDP broadcast from Telemetry Hub."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    
    print(f"Listening on {host}:{port}...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            data, addr = sock.recvfrom(1024)
            payload = json.loads(data.decode())
            
            telemetry = Telemetry(
                timestamp=payload["timestamp"],
                gforce_x=payload["gforce"]["x"],
                gforce_y=payload["gforce"]["y"],
                gforce_z=payload["gforce"]["z"],
                roll=payload["orientation"]["roll"],
                pitch=payload["orientation"]["pitch"],
                heave=payload["orientation"]["heave"],
                impact_detected=payload["impact"]["detected"],
                impact_magnitude=payload["impact"]["magnitude"],
            )
            
            # Print formatted output
            print(f"\rG-Force: X={telemetry.gforce_x:+.2f}G Y={telemetry.gforce_y:+.2f}G Z={telemetry.gforce_z:+.2f}G | "
                  f"Pitch={telemetry.pitch:+.1f}° Roll={telemetry.roll:+.1f}° | "
                  f"Impact: {telemetry.impact_detected}", end="")
            
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n\nShutdown.")
        sock.close()


def tcp_consumer(host="127.0.0.1", port=5050):
    """Connect via TCP to Telemetry Hub daemon."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    print(f"Connected to {host}:{port}...")
    print("Press Ctrl+C to disconnect\n")

    buf = b""
    try:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            buf += data
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                payload = json.loads(line.decode())
                print(json.dumps(payload, indent=2))
    except KeyboardInterrupt:
        print("\n\nDisconnected.")
    finally:
        sock.close()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "udp"
    
    if mode == "udp":
        udp_consumer()
    elif mode == "tcp":
        tcp_consumer()
    else:
        print(f"Usage: {sys.argv[0]} [udp|tcp]")
        sys.exit(1)
