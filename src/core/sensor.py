from typing import List, Dict, Tuple
import numpy as np
from .patterns import SensorPattern
from .privacy import PrivacyMetrics
from .models import PatternPredictor


class EnhancedSensor:
    """Enhanced sensor with pattern learning and privacy preservation"""

    def __init__(self, name: str, location: Tuple[float, float], pattern_type: str):
        self.name = name
        self.location = location
        self.pattern = SensorPattern(pattern_type)
        self.privacy = PrivacyMetrics()
        self.predictor = PatternPredictor()

        # History tracking
        self.temperature_history: List[float] = []
        self.prediction_history: List[float] = []
        self.accuracy_history: List[float] = [0.5]  # Start at 50% accuracy
        self.learned_patterns: Dict = {}

        # Base temperature configuration
        self.base_temp = {
            'factory': 25 + np.random.normal(0, 2),
            'office': 22 + np.random.normal(0, 1),
            'outdoor': 20 + np.random.normal(0, 3)
        }[pattern_type]

    def generate_temperature(self, hour: int) -> float:
        """Generate temperature with detailed patterns"""
        # Base temperature with daily cycle
        temp = self.base_temp + 3 * np.sin(2 * np.pi * hour / 24)

        # Add pattern-specific variations
        temp += self.pattern.get_event_impact(hour)

        # Add noise
        temp += np.random.normal(0, 0.5)

        self.temperature_history.append(temp)

        # Train predictor on new data
        self.predictor.train(self.temperature_history)

        return temp

    def learn_patterns(self, window_size: int = 24) -> Dict:
        """Analyze and learn patterns from recent data"""
        if len(self.temperature_history) < window_size:
            return {}

        recent_data = self.temperature_history[-window_size:]

        # Calculate actual metrics for patterns
        mean_temp = np.mean(recent_data)
        std_temp = np.std(recent_data)

        # Update accuracy based on prediction performance
        if len(self.prediction_history) > 0:
            prediction_error = abs(self.prediction_history[-1] - recent_data[-1])
            accuracy = max(0, 1 - prediction_error / mean_temp)
            self.accuracy_history.append(
                0.9 * self.accuracy_history[-1] + 0.1 * accuracy
            )

        patterns = {
            'daily_range': (min(recent_data), max(recent_data)),
            'variance': np.var(recent_data),
            'trend': np.polyfit(range(len(recent_data)), recent_data, 1)[0],
            'peak_hours': self._find_peak_hours(recent_data)
        }

        self.learned_patterns = patterns
        return patterns

    def _find_peak_hours(self, data: List[float]) -> List[int]:
        """Identify hours with peak temperatures"""
        mean_temp = np.mean(data)
        peak_hours = [i for i, temp in enumerate(data)
                      if temp > mean_temp + np.std(data)]
        return peak_hours

    def predict_next_temperature(self) -> float:
        """Predict next temperature value"""
        prediction = self.predictor.predict(self.temperature_history)
        if prediction is not None:
            self.prediction_history.append(prediction)
        return prediction if prediction is not None else self.temperature_history[-1]

    def get_metrics(self) -> Dict:
        """Get comprehensive sensor metrics"""
        return {
            'privacy': self.privacy.get_metrics(),
            'accuracy': self.accuracy_history[-1] if self.accuracy_history else 0,
            'training': self.predictor.get_training_metrics(),
            'patterns': self.learned_patterns
        }