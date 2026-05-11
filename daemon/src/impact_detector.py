#!/usr/bin/env python3
"""Impact and collision detection."""

import math
from collections import deque
from typing import Dict, Any, Optional


class ImpactDetector:
    """Detects impacts and collisions from G-force spikes."""
    
    def __init__(self, threshold: float = 0.3, window_size: int = 5):
        """Initialize detector.
        
        Args:
            threshold: G-force magnitude threshold for impact (0.0-1.0)
            window_size: Number of samples to track for moving average
        """
        self.threshold = threshold
        self.window_size = window_size
        self.history = deque(maxlen=window_size)
    
    def detect(self, parsed: Dict[str, Any]) -> Dict[str, Any]:
        """Detect impacts from telemetry.
        
        Args:
            parsed: Output from DBoxParser
            
        Returns:
            Dict with impact info
        """
        # Calculate total G-force magnitude
        gx = parsed.get('gforce_x', 0.0)
        gy = parsed.get('gforce_y', 0.0)
        gz = parsed.get('gforce_z', 0.0)
        
        magnitude = math.sqrt(gx**2 + gy**2 + gz**2)
        self.history.append(magnitude)
        
        # Calculate moving average
        avg_magnitude = sum(self.history) / len(self.history) if self.history else 0.0
        
        # Detect spike (sudden increase above threshold)
        detected = magnitude > (avg_magnitude + self.threshold)
        
        # Calculate impact direction
        direction = None
        if detected and magnitude > 0:
            direction = {
                'x': gx / magnitude,
                'y': gy / magnitude,
                'z': gz / magnitude,
            }
        
        return {
            'detected': detected,
            'magnitude': magnitude,
            'direction': direction,
        }
