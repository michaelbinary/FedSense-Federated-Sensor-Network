#!/usr/bin/env python3
"""
Basic demonstration of the Federated Sensor Network.
Shows pattern learning, privacy preservation, and visualization capabilities.
"""

from fedsense.network.federation import EnhancedFederatedNetwork
from fedsense.visualization.console import NetworkConsole
from rich.console import Console
import time

console = Console()


def main():
    """Run a basic demonstration simulation"""
    network_console = NetworkConsole()
    network_console.print_simulation_header()

    # Initialize network
    network = EnhancedFederatedNetwork()

    try:
        # Run simulation
        total_hours = 100
        for hour in range(total_hours):
            # Update network
            network.update(hour)

            # Print progress updates
            if hour % 10 == 0:
                network_console.print_simulation_progress(hour, total_hours)
                metrics = network.get_network_metrics()
                network_console.print_network_health(metrics)
                network_console.print_sensor_analysis(network.sensors)

            time.sleep(0.2)

        # Show final results
        network_console.print_simulation_complete()

        # Display final visualization
        network.plotter.show()

    except KeyboardInterrupt:
        console.print("\n[red]Simulation interrupted by user[/red]")
    except Exception as e:
        network_console.print_error(e)
        raise


if __name__ == "__main__":
    main()