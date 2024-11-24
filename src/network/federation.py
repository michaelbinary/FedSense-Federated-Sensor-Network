import numpy as np
from typing import List, Dict
from ..core.sensor import EnhancedSensor
from ..visualization.plotter import NetworkPlotter
from rich.console import Console

console = Console()


class EnhancedFederatedNetwork:
    """Manages a network of federated sensors with visualization"""

    def __init__(self):
        self.sensors = [
            EnhancedSensor("Factory Floor", (0, 0), "factory"),
            EnhancedSensor("Office Building", (1, 0), "office"),
            EnhancedSensor("Outdoor Area", (2, 0), "outdoor")
        ]

        self.current_hour = 0
        self.global_predictions = []
        self.pattern_library = {}

        # Initialize visualization
        self.plotter = NetworkPlotter()

    def update(self, hour: int):
        """Update network state"""
        self.current_hour = hour

        # Update each sensor
        for sensor in self.sensors:
            temp = sensor.generate_temperature(hour)
            patterns = sensor.learn_patterns()
            sensor.privacy.update(temp, bool(patterns))

            if patterns:
                self.pattern_library[sensor.name] = patterns

        # Update visualization
        self.plotter.update_plots(self.sensors, hour)

    def get_network_metrics(self) -> Dict:
        """Get comprehensive network metrics"""
        return {
            'sensors': {
                sensor.name: sensor.get_metrics()
                for sensor in self.sensors
            },
            'global_patterns': self.pattern_library,
            'network_health': self._calculate_network_health()
        }

    def _calculate_network_health(self) -> Dict:
        """Calculate overall network health metrics"""
        accuracies = [s.accuracy_history[-1] for s in self.sensors]
        privacy_scores = [s.privacy.privacy_score for s in self.sensors]

        return {
            'average_accuracy': np.mean(accuracies),
            'average_privacy': np.mean(privacy_scores),
            'active_sensors': len(self.sensors),
            'pattern_coverage': len(self.pattern_library) / len(self.sensors)
        }

    def run_simulation(self, hours: int = 100):
        """Run the complete simulation"""
        console.print("[bold blue]Enhanced Federated Learning Simulation[/bold blue]")
        console.print("\n[yellow]Showing detailed pattern analysis and privacy metrics[/yellow]")

        try:
            for hour in range(hours):
                self.update(hour)

                if hour % 10 == 0:
                    metrics = self.get_network_metrics()
                    health = metrics['network_health']
                    console.print(f"\n[cyan]Hour {hour}[/cyan]")
                    console.print(f"Network Health:")
                    console.print(f"  Accuracy: {health['average_accuracy']:.2%}")
                    console.print(f"  Privacy: {health['average_privacy']:.1f}%")
                    console.print(f"  Pattern Coverage: {health['pattern_coverage']:.1%}")

        except KeyboardInterrupt:
            console.print("\n[red]Simulation interrupted by user[/red]")

        console.print("\n[bold green]Simulation Complete![/bold green]")
        self.plotter.show()