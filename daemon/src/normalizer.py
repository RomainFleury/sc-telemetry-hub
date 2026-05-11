#!/usr/bin/env python3
"""Telemetry data normalizer and formatter."""

import json
import time
from typing import Dict, Any


class TelemetryNormalizer:
    """Normalizes parsed telemetry data to standard format."""
    
    @staticmethod
    def normalize(parsed: Dict[str, Any], impact: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize parsed telemetry to standard format.
        
        Args:
            parsed: Output from DBoxParser
            impact: Output from ImpactDetector
            
        Returns:
            Normalized telemetry dict
        """
        return {
            'timestamp': time.time(),
            'gforce': {
                'x': float(parsed.get('gforce_x', 0.0)),
                'y': float(parsed.get('gforce_y', 0.0)),
                'z': float(parsed.get('gforce_z', 0.0)),
            },
            'orientation': {
                'roll': float(parsed.get('roll', 0.0)),
                'pitch': float(parsed.get('pitch', 0.0)),
                'heave': float(parsed.get('heave', 0.0)),
            },
            'impact': impact,
        }
    
    @staticmethod
    def to_json(telemetry: Dict[str, Any]) -> str:
        """Convert to JSON string.
        
        Args:
            telemetry: Normalized telemetry dict
            
        Returns:
            JSON string
        """
        return json.dumps(telemetry)
    
    @staticmethod
    def to_json_bytes(telemetry: Dict[str, Any]) -> bytes:
        """Convert to JSON bytes.
        
        Args:
            telemetry: Normalized telemetry dict
            
        Returns:
            JSON bytes
        """
        return TelemetryNormalizer.to_json(telemetry).encode('utf-8')
