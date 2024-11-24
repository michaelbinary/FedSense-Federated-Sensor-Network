from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import List, Dict
from ..core.sensor import EnhancedSensor

class NetworkConsole:
    """Handles console output and formatting"""

    def __init__(self):
        self.console = Console()

    def print_simulation_header(self):
        """Print simulation start header"""
        self.console.print("[bold blue]Enhanced Federated Learning Simulation[/bold blue]")
        self.console.print("\n[yellow]Showing detailed pattern analysis and privacy metrics[/yellow]")

    def print_sensor_analysis(self, sensors: List[EnhancedSensor]):
        """Print detailed sensor analysis"""
        table = Table(title="Detailed Pattern Analysis")
        table.add_column("Sensor")
        table.add_column("Learned Patterns")
        table.add_column("Privacy Score")
        table.add_column("Accuracy")

        for sensor in sensors:
            patterns = sensor.learned_patterns
            if patterns:
                pattern_str = (
                    f"Range: {patterns['daily_range']}\n"
                    f"Variance: {patterns['variance']:.2f}\n"
                    f"Trend: {patterns['trend']:.2f}"
                )

                table.add_row(
                    sensor.name,
                    pattern_str,
                    f"{sensor.privacy.privacy_score:.1f}%",
                    f"{sensor.accuracy_history[-1]:.2%}"
                )

        self.console.print(table)

    def print_network_health(self, metrics: Dict):
        """Print network health metrics"""
        health = metrics['network_health']
        panel = Panel(
            f"Network Health Metrics\n\n"
            f"Average Accuracy: {health['average_accuracy']:.2%}\n"
            f"Average Privacy: {health['average_privacy']:.1f}%\n"
            f"Active Sensors: {health['active_sensors']}\n"
            f"Pattern Coverage: {health['pattern_coverage']:.1%}",
            title="Network Status"
        )
        self.console.print(panel)

    def print_simulation_progress(self, hour: int, total_hours: int):
        """Print simulation progress"""
        self.console.print(f"[cyan]Hour {hour}/{total_hours} "
                         f"({hour/total_hours:.1%} complete)[/cyan]")

    def print_error(self, error: Exception):
        """Print error message"""
        self.console.print(f"[bold red]Error: {str(error)}[/bold red]")

    def print_simulation_complete(self):
        """Print simulation completion message"""
        self.console.print("\n[bold green]Simulation Complete![/bold green]")