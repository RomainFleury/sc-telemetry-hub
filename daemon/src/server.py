#!/usr/bin/env python3
"""Telemetry Hub server - main daemon."""

from __future__ import annotations

import json
import logging
import select
import socket
import threading
import time
from collections import deque
from typing import List

from .impact_detector import ImpactDetector
from .normalizer import TelemetryNormalizer
from .parser import DBoxParser

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S")
    )
    logger.addHandler(handler)


class TelemetryServer:
    """Main telemetry server."""

    def __init__(
        self,
        host: str = "127.0.0.1",
        tcp_port: int = 5050,
        broadcast_port: int = 5555,
        dbox_port: int = 33740,
    ) -> None:
        self.host = host
        self.tcp_port = tcp_port
        self.broadcast_port = broadcast_port
        self.dbox_port = dbox_port

        self.running = False
        self.clients: List[socket.socket] = []
        self.impact_detector = ImpactDetector()

        self.telemetry_buffer: deque = deque(maxlen=100)
        self.lock = threading.Lock()

        self._tcp_server_sock: socket.socket | None = None
        self._udp_in_sock: socket.socket | None = None

    def start(self) -> None:
        self.running = True

        threading.Thread(target=self._run_udp_listener, daemon=True).start()
        threading.Thread(target=self._run_tcp_server, daemon=True).start()
        threading.Thread(target=self._run_broadcaster, daemon=True).start()

        logger.info("Telemetry Hub server started")
        logger.info("   UDP input (D-BOX): %s:%s", self.host, self.dbox_port)
        logger.info("   TCP server (UI):   %s:%s", self.host, self.tcp_port)
        logger.info("   UDP send target:   %s:%s", self.host, self.broadcast_port)
        logger.info("Press Ctrl+C to shutdown...")

        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        logger.info("Shutting down...")
        self.running = False

        if self._tcp_server_sock:
            try:
                self._tcp_server_sock.close()
            except OSError:
                pass
            self._tcp_server_sock = None

        if self._udp_in_sock:
            try:
                self._udp_in_sock.close()
            except OSError:
                pass
            self._udp_in_sock = None

        with self.lock:
            for client in self.clients:
                try:
                    client.close()
                except OSError:
                    pass
            self.clients.clear()

    def _run_udp_listener(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._udp_in_sock = sock

        try:
            sock.bind((self.host, self.dbox_port))
            logger.info("UDP listener ready on port %s", self.dbox_port)

            packet_count = 0
            while self.running:
                try:
                    sock.settimeout(0.5)
                    try:
                        data, addr = sock.recvfrom(2048)
                    except socket.timeout:
                        continue
                    packet_count += 1

                    parsed = DBoxParser.parse(data)
                    if parsed:
                        impact = self.impact_detector.detect(parsed)
                        normalized = TelemetryNormalizer.normalize(parsed, impact)
                        with self.lock:
                            self.telemetry_buffer.append(normalized)

                        if packet_count % 60 == 0:
                            logger.info("Processed %s packets", packet_count)
                    else:
                        logger.warning("Failed to parse packet from %s", addr)

                except OSError:
                    if not self.running:
                        break
                    logger.exception("UDP listener error")
        except OSError as e:
            logger.error("UDP listener failed: %s", e)
        finally:
            sock.close()

    def _run_tcp_server(self) -> None:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._tcp_server_sock = server

        try:
            server.bind((self.host, self.tcp_port))
            server.listen(5)
            server.settimeout(0.5)
            logger.info("TCP server ready on port %s", self.tcp_port)

            while self.running:
                try:
                    try:
                        client, addr = server.accept()
                    except socket.timeout:
                        continue
                    logger.info("Client connected: %s", addr)

                    with self.lock:
                        self.clients.append(client)

                    threading.Thread(
                        target=self._handle_client,
                        args=(client, addr),
                        daemon=True,
                    ).start()
                except OSError:
                    if not self.running:
                        break
                    if self.running:
                        logger.exception("TCP server error")
        except OSError as e:
            logger.error("TCP server failed: %s", e)
        finally:
            server.close()

    def _handle_client(self, client: socket.socket, addr) -> None:
        buf = b""
        try:
            while self.running:
                r, _, _ = select.select([client], [], [], 0.1)
                if r:
                    chunk = client.recv(4096)
                    if not chunk:
                        break
                    buf += chunk
                    while b"\n" in buf:
                        line, buf = buf.split(b"\n", 1)
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            msg = json.loads(line.decode())
                        except json.JSONDecodeError:
                            continue
                        cmd = msg.get("command")
                        if cmd == "shutdown":
                            reply = json.dumps({"status": "ok", "message": "shutting down"})
                            try:
                                client.sendall(reply.encode() + b"\n")
                            except OSError:
                                pass
                            self.stop()
                            return
                        if cmd == "ping":
                            reply = json.dumps(
                                {"status": "ok", "message": "pong"},
                                separators=(",", ":"),
                            )
                            try:
                                client.sendall(reply.encode() + b"\n")
                            except OSError:
                                pass

                with self.lock:
                    if self.telemetry_buffer:
                        latest = self.telemetry_buffer[-1]
                        payload = TelemetryNormalizer.to_json_bytes(latest) + b"\n"
                        try:
                            client.sendall(payload)
                        except OSError:
                            break
        except (ConnectionResetError, BrokenPipeError, OSError) as e:
            logger.debug("Client %s disconnected: %s", addr, e)
        finally:
            with self.lock:
                try:
                    self.clients.remove(client)
                except ValueError:
                    pass
            try:
                client.close()
            except OSError:
                pass

    def _run_broadcaster(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            while self.running:
                with self.lock:
                    if self.telemetry_buffer:
                        latest = self.telemetry_buffer[-1]
                        data = TelemetryNormalizer.to_json_bytes(latest)
                        try:
                            sock.sendto(data, (self.host, self.broadcast_port))
                        except OSError as e:
                            logger.debug("Broadcast error: %s", e)

                time.sleep(0.016)
        except Exception as e:
            logger.error("Broadcaster error: %s", e)
        finally:
            sock.close()
