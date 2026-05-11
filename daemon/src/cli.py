#!/usr/bin/env python3
"""Command-line interface for Telemetry Hub daemon."""

from __future__ import annotations

import json
import socket
import sys
import time

import click

from .server import TelemetryServer


@click.group()
def cli() -> None:
    """Star Citizen Telemetry Hub."""
    pass


@cli.group()
def daemon() -> None:
    """Manage the telemetry daemon."""
    pass


@daemon.command("start")
@click.option("--host", default="127.0.0.1", help="Listen host")
@click.option("--port", default=5050, help="TCP server port")
@click.option("--broadcast-port", default=5555, help="UDP output port (unicast to host)")
@click.option("--dbox-port", default=33740, help="D-BOX input port")
def daemon_start(host: str, port: int, broadcast_port: int, dbox_port: int) -> None:
    """Start the telemetry daemon."""
    click.echo("Starting Telemetry Hub daemon...")
    click.echo(f"   D-BOX input: {host}:{dbox_port}")
    click.echo(f"   TCP server: {host}:{port}")
    click.echo(f"   UDP output: {host}:{broadcast_port}")
    click.echo()

    server = TelemetryServer(
        host=host,
        tcp_port=port,
        broadcast_port=broadcast_port,
        dbox_port=dbox_port,
    )

    try:
        server.start()
    except KeyboardInterrupt:
        click.echo("\nShutting down...")
        server.stop()
        sys.exit(0)


@daemon.command("status")
@click.option("--port", default=5050, help="TCP server port")
@click.option("--host", default="127.0.0.1", help="Daemon host")
def daemon_status(host: str, port: int) -> None:
    """Check daemon status."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()

        if result == 0:
            click.echo(f"Daemon is running on {host}:{port}")
        else:
            click.echo(f"Daemon is not reachable at {host}:{port}")
            sys.exit(1)
    except OSError as e:
        click.echo(f"Error checking status: {e}")
        sys.exit(1)


@daemon.command("stop")
@click.option("--port", default=5050, help="TCP server port")
@click.option("--host", default="127.0.0.1", help="Daemon host")
def daemon_stop(host: str, port: int) -> None:
    """Stop the running daemon."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((host, port))
        sock.sendall(b'{"command":"shutdown"}\n')
        sock.close()
        click.echo("Shutdown signal sent")
    except ConnectionRefusedError:
        click.echo("Daemon is not running")
        sys.exit(1)
    except OSError as e:
        click.echo(f"Error: {e}")
        sys.exit(1)


@cli.command()
@click.option("--port", default=5050, help="TCP server port")
@click.option("--host", default="127.0.0.1", help="Daemon host")
def ping(host: str, port: int) -> None:
    """Test daemon connectivity."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.3)
        sock.connect((host, port))
        sock.sendall(b'{"command":"ping"}\n')

        buf = b""
        deadline = time.time() + 3.0
        while time.time() < deadline:
            try:
                chunk = sock.recv(4096)
            except socket.timeout:
                chunk = b""
            if not chunk:
                continue
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    result = json.loads(line.decode())
                except json.JSONDecodeError:
                    continue
                if result.get("status") == "ok" and result.get("message") == "pong":
                    sock.close()
                    click.echo(result.get("message", "ok"))
                    return
        sock.close()
        click.echo("No pong received (daemon may still be running).")
        sys.exit(1)
    except ConnectionRefusedError:
        click.echo("Cannot connect to daemon (is it running?)")
        sys.exit(1)
    except (json.JSONDecodeError, OSError) as e:
        click.echo(f"Error: {e}")
        sys.exit(1)


@cli.command("discover")
@click.option("--host", default="0.0.0.0", help="Bind address")
@click.option("--port", default=33740, help="UDP port to listen on")
@click.option("--max", "max_packets", default=30, help="Packets to log then exit")
def discover(host: str, port: int, max_packets: int) -> None:
    """Log hex dumps of incoming UDP packets (use while Star Citizen sends telemetry)."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    click.echo(f"Listening on {host}:{port}, logging {max_packets} packets (Ctrl+C to stop)...")

    count = 0
    try:
        while count < max_packets:
            data, addr = sock.recvfrom(2048)
            count += 1
            hx = data.hex()
            spaced = " ".join(hx[i : i + 2] for i in range(0, len(hx), 2))
            click.echo(f"[{count}] {len(data)} bytes from {addr[0]}:{addr[1]}")
            click.echo(spaced[:400] + ("..." if len(spaced) > 400 else ""))
    except KeyboardInterrupt:
        click.echo("Stopped.")
    finally:
        sock.close()


@cli.command("test-parser")
@click.argument("packet_hex")
def test_parser(packet_hex: str) -> None:
    """Parse a single packet from hex (same format as discover output, spaces ok)."""
    from .parser import DBoxParser

    parsed = DBoxParser.parse_hex(packet_hex)
    if not parsed:
        click.echo("Parse failed (layout may not match packet).")
        sys.exit(1)
    click.echo(json.dumps(parsed, indent=2))


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
