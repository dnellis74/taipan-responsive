"""Port model for Taipan."""

from dataclasses import dataclass, field
from typing import Dict, List
import random

from taipan.models.commodity import Commodity

# List of all port names in the game
PORT_NAMES = [
    "At Sea", "Hong Kong", "Shanghai", "Nagasaki",
    "Saigon", "Manila", "Singapore", "Batavia"
]

# Base prices for each commodity at each port
BASE_PRICES = {
    Commodity.OPIUM: [1000, 11, 16, 15, 14, 12, 10, 13],
    Commodity.SILK: [100, 11, 14, 15, 16, 10, 13, 12],
    Commodity.ARMS: [10, 12, 16, 10, 11, 13, 14, 15],
    Commodity.GENERAL: [1, 10, 11, 12, 13, 14, 15, 16],
}

@dataclass
class Port:
    """Port location and trading information."""
    name: str

    def get_price(self, commodity: Commodity) -> int:
        """Get current price for a commodity."""
        port_index = self.get_port_index()
        base_price = BASE_PRICES[commodity][port_index]
        fluctuation = random.randint(-2, 2)  # Small random fluctuation
        return max(1, base_price + fluctuation)

    def get_port_index(self) -> int:
        """Get the port's index in the original game's port list."""
        return PORT_NAMES.index(self.name)

    @classmethod
    def initialize_ports(cls) -> List['Port']:
        """Initialize all ports in the game."""
        ports = [
            cls(name="At Sea"),
            cls(name="Hong Kong"),
            cls(name="Shanghai"),
            cls(name="Nagasaki"),
            cls(name="Saigon"),
            cls(name="Manila"),
            cls(name="Singapore"),
            cls(name="Batavia"),
        ]
        return ports 