#!/usr/bin/env python3
import click
from rich.console import Console
from .network.federation import EnhancedFederatedNetwork
from .visualization.console import NetworkConsole

console = Console()


@click.group()
def cli():
    """Federated Sensor Network (FedSense) Command Line Interface"""
    pass


@cli.command()
@click.option('--hours', default=100, help='Number of simulation hours')
@click.option('--sensors', default=3, help='Number of sensors')
@click.option('--interval', default=0.2, help='Update interval in seconds')
@click.option('--output', default=None, help='Output directory for results')
def run(hours, sensors, interval, output):
    """Run a federated sensor network simulation"""
    try:
        network = EnhancedFederatedNetwork()
        network_console = NetworkConsole()

        network_console.print_simulation_header()

        # Run simulation
        network.run_simulation(hours)

        # Save results if output specified
        if output:
            network.plotter.save(f"{output}/simulation_final.png")

    except Exception as e:
        network_console.print_error(e)
        raise


@cli.command()
def info():
    """Display information about the system"""
    console.print("""
[bold blue]Federated Sensor Network (FedSense)[/bold blue]

[yellow]Components:[/yellow]
- Enhanced Sensors with pattern learning
- Privacy-preserving data sharing
- Real-time pattern analysis
- Interactive visualization

[yellow]Parameters:[/yellow]
- Simulation Hours: Duration of simulation
- Number of Sensors: Size of sensor network
- Update Interval: Time between updates
- Output Directory: Location for saving results

[yellow]Example Usage:[/yellow]
  # Run basic simulation
  fedsense run

  # Run extended simulation
  fedsense run --hours 200 --sensors 5

  # Save results
  fedsense run --output ./results
    """)


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()