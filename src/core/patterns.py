import numpy as np
from typing import Dict, Tuple

class SensorPattern:
    """Defines specific patterns for each sensor type"""

    def __init__(self, pattern_type: str):
        self.pattern_type = pattern_type
        self.known_events = {
            'factory': {
                'startup': (8, 2),  # (hour, duration)
                'shutdown': (17, 1),
                'lunch_break': (12, 1)
            },
            'office': {
                'morning_hvac': (7, 2),
                'peak_occupancy': (14, 3),
                'evening_shutdown': (18, 2)
            },
            'outdoor': {
                'sunrise': (6, 3),
                'peak_heat': (14, 4),
                'sunset': (18, 3)
            }
        }

    def get_event_impact(self, hour: int) -> float:
        """Calculate temperature impact of known events"""
        events = self.known_events.get(self.pattern_type, {})
        impact = 0

        for event, (start_hour, duration) in events.items():
            if start_hour <= hour % 24 < start_hour + duration:
                if 'startup' in event:
                    impact += 4 * np.sin(np.pi * ((hour % 24) - start_hour) / duration)
                elif 'shutdown' in event:
                    impact -= 2 * np.sin(np.pi * ((hour % 24) - start_hour) / duration)
                elif 'hvac' in event:
                    impact += 2 * np.cos(2 * np.pi * ((hour % 24) - start_hour) / duration)
                else:
                    impact += np.random.normal(1, 0.2)

        return impact

    def add_custom_event(self, name: str, start_hour: int, duration: int):
        """Add a custom event to the pattern"""
        if self.pattern_type not in self.known_events:
            self.known_events[self.pattern_type] = {}
        self.known_events[self.pattern_type][name] = (start_hour, duration)