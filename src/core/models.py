import torch
import torch.nn as nn
from typing import Optional, List


class SensorModel(nn.Module):
    def __init__(self, input_size: int = 24, hidden_size: int = 48):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Linear(hidden_size // 2, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.model(x)


class PatternPredictor:
    def __init__(self):
        self.model = SensorModel()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        self.training_history: List[float] = []

    def train(self, data: List[float], window_size: int = 24):
        """Train the model on recent data"""
        if len(data) < window_size + 1:
            return

        x_data = []
        y_data = []

        for i in range(len(data) - window_size):
            x_data.append(data[i:i + window_size])
            y_data.append(data[i + window_size])

        x_tensor = torch.FloatTensor(x_data)
        y_tensor = torch.FloatTensor(y_data)

        self.model.train()
        self.optimizer.zero_grad()

        outputs = self.model(x_tensor)
        loss = self.criterion(outputs, y_tensor.unsqueeze(1))

        loss.backward()
        self.optimizer.step()

        self.training_history.append(loss.item())

    def predict(self, data: List[float], window_size: int = 24) -> Optional[float]:
        """Predict next value based on recent data"""
        if len(data) < window_size:
            return None

        self.model.eval()
        with torch.no_grad():
            x = torch.FloatTensor(data[-window_size:]).unsqueeze(0)
            prediction = self.model(x)
            return prediction.item()

    def get_training_metrics(self) -> dict:
        """Get model training metrics"""
        if not self.training_history:
            return {'average_loss': None, 'loss_trend': None}

        return {
            'average_loss': sum(self.training_history) / len(self.training_history),
            'loss_trend': (self.training_history[-1] - self.training_history[0])
            if len(self.training_history) > 1 else 0
        }