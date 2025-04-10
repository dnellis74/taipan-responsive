"""Core game state models for Taipan."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random

from taipan.models.player import Player
from taipan.models.port import Port
from taipan.models.ship import Ship
from taipan.models.commodity import Commodity

@dataclass
class GameState:
    """Current state of the game."""
    player: Player
    ports: List[Port] = field(default_factory=Port.initialize_ports)
    current_port: Port = field(init=False)
    ship: Ship = field(default_factory=Ship)
    day: int = 1
    month: int = 1
    year: int = 1860
    li_yuen_visited: bool = False
    wu_warning: bool = False
    wu_bailout: int = 0
    enemy_strength: float = 20.0
    enemy_damage: float = 0.5

    def __post_init__(self):
        """Initialize the game state."""
        self.current_port = self.ports[1]  # Start in Hong Kong

    def get_port_by_name(self, name: str) -> Optional[Port]:
        """Get a port by its name."""
        for port in self.ports:
            if port.name == name:
                return port
        return None

    def get_port_by_index(self, index: int) -> Optional[Port]:
        """Get a port by its index."""
        if 0 <= index < len(self.ports):
            return self.ports[index]
        return None

    def get_current_port_index(self) -> int:
        """Get the index of the current port."""
        for i, port in enumerate(self.ports):
            if port.name == self.current_port.name:
                return i
        raise ValueError("Current port not found in ports list")

    def set_current_port(self, port: Port) -> None:
        """Set the current port."""
        self.current_port = port

    def advance_time(self, days: int) -> None:
        """Advance the game time by the specified number of days."""
        self.day += days
        while self.day > 30:
            self.day -= 30
            self.month += 1
            if self.month > 12:
                self.month = 1
                self.year += 1 