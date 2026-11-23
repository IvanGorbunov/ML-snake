import torch
from torch import nn


class QNetwork(nn.Module):
    """The model"""

    def __init__(self) -> None:
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(11, 256), nn.ReLU(), nn.Linear(256, 3))
