import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from typing import List
from ..core.sensor import EnhancedSensor


class NetworkPlotter:
    """Handles all visualization aspects of the network"""

    def __init__(self):
        plt.style.use('dark_background')
        self.fig = plt.figure(figsize=(15, 10))
        self.gs = GridSpec(4, 3, figure=self.fig)
        self.setup_plots()

        self.colors = ['#FF9999', '#99FF99', '#9999FF']
        self.fig.patch.set_facecolor('#1C1C1C')
        plt.tight_layout()

    def setup_plots(self):
        """Initialize all plot areas"""
        # Main temperature plot
        self.temp_ax = self.fig.add_subplot(self.gs[0, :])

        # Individual sensor plots
        self.sensor_axes = [
            self.fig.add_subplot(self.gs[1, i]) for i in range(3)
        ]

        # Pattern analysis plot
        self.pattern_ax = self.fig.add_subplot(self.gs[2, :])

        # Privacy metrics plot
        self.privacy_ax = self.fig.add_subplot(self.gs[3, :])

    def update_plots(self, sensors: List[EnhancedSensor], hour: int):
        """Update all visualization components"""
        self._clear_plots()
        self._plot_temperatures(sensors)
        self._plot_sensor_insights(sensors)
        self._plot_pattern_analysis(sensors)
        self._plot_privacy_metrics(sensors)

        plt.tight_layout()
        plt.pause(0.1)

    def _clear_plots(self):
        """Clear all plots for updating"""
        for ax in [self.temp_ax, self.pattern_ax, self.privacy_ax] + self.sensor_axes:
            ax.clear()

    def _plot_temperatures(self, sensors: List[EnhancedSensor]):
        """Plot main temperature readings"""
        window = min(48, len(sensors[0].temperature_history))

        for i, sensor in enumerate(sensors):
            data = sensor.temperature_history[-window:]
            times = list(range(len(data)))
            self.temp_ax.plot(times, data, label=sensor.name, color=self.colors[i])

        self.temp_ax.set_title("Temperature Readings with Pattern Detection", color='white')
        self.temp_ax.legend(loc='upper right')
        self.temp_ax.grid(True, alpha=0.2)

    def _plot_sensor_insights(self, sensors: List[EnhancedSensor]):
        """Plot individual sensor accuracy trends"""
        window = min(48, len(sensors[0].temperature_history))

        for i, (sensor, ax) in enumerate(zip(sensors, self.sensor_axes)):
            if len(sensor.accuracy_history) > 0:
                acc_data = sensor.accuracy_history[-window:]
                times = list(range(len(acc_data)))
                ax.plot(times, acc_data, color=self.colors[i])
                ax.set_title(f"{sensor.name}\nAccuracy: {acc_data[-1]:.2%}")
                ax.set_ylim(0, 1)
                ax.grid(True, alpha=0.2)

    def _plot_pattern_analysis(self, sensors: List[EnhancedSensor]):
        """Plot pattern analysis results"""
        self.pattern_ax.set_title("Pattern Analysis", color='white')

        for i, sensor in enumerate(sensors):
            if len(sensor.temperature_history) >= 24:
                data = sensor.temperature_history[-24:]
                times = list(range(len(data)))
                self.pattern_ax.plot(
                    times,
                    data,
                    label=f"{sensor.name}",
                    color=self.colors[i]
                )

        self.pattern_ax.legend(loc='upper right')
        self.pattern_ax.grid(True, alpha=0.2)

    def _plot_privacy_metrics(self, sensors: List[EnhancedSensor]):
        """Plot privacy preservation metrics"""
        sensor_names = [s.name for s in sensors]
        privacy_scores = [s.privacy.privacy_score for s in sensors]
        bars = self.privacy_ax.bar(sensor_names, privacy_scores, color=self.colors)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            self.privacy_ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f'{height:.1f}%',
                ha='center', va='bottom'
            )

        self.privacy_ax.set_title("Privacy Preservation Scores", color='white')
        self.privacy_ax.set_ylim(0, 100)
        self.privacy_ax.grid(True, alpha=0.2)

    def show(self):
        """Display the final plot"""
        plt.show()

    def save(self, filename: str):
        """Save the current plot to a file"""
        self.fig.savefig(filename, bbox_inches='tight', facecolor='#1C1C1C')