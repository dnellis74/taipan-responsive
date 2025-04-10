"""Core game state models for Taipan."""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List

class Port(Enum):
    """Available ports in the game."""
    AT_SEA = auto()
    HONG_KONG = auto()
    SHANGHAI = auto()
    NAGASAKI = auto()
    SAIGON = auto()
    MANILA = auto()
    SINGAPORE = auto()
    BATAVIA = auto()

class Commodity(Enum):
    """Tradeable commodities."""
    OPIUM = auto()
    SILK = auto()
    ARMS = auto()
    GENERAL = auto()

@dataclass
class Ship:
    """Player's ship status."""
    capacity: int = 60
    damage: int = 0
    guns: int = 0
    hold: Dict[Commodity, int] = field(default_factory=lambda: {c: 0 for c in Commodity})

@dataclass
class Player:
    """Player's status including finances and firm name."""
    firm_name: str = ""
    cash: int = 0
    bank: int = 0
    debt: int = 0
    ship: Ship = field(default_factory=Ship)

@dataclass
class Market:
    """Market prices and conditions."""
    prices: Dict[Commodity, Dict[Port, int]] = field(
        default_factory=lambda: {
            c: {p: 0 for p in Port} for c in Commodity
        }
    )
    base_prices: Dict[Commodity, Dict[Port, int]] = field(
        default_factory=lambda: {
            Commodity.OPIUM: {p: v for p, v in zip(Port, [1000, 11, 16, 15, 14, 12, 10, 13])},
            Commodity.SILK: {p: v for p, v in zip(Port, [100, 11, 14, 15, 16, 10, 13, 12])},
            Commodity.ARMS: {p: v for p, v in zip(Port, [10, 12, 16, 10, 11, 13, 14, 15])},
            Commodity.GENERAL: {p: v for p, v in zip(Port, [1, 10, 11, 12, 13, 14, 15, 16])},
        }
    )

@dataclass
class GameState:
    """Overall game state."""
    player: Player = field(default_factory=Player)
    market: Market = field(default_factory=Market)
    current_port: Port = Port.HONG_KONG
    month: int = 1
    year: int = 1860
    li_yuen_visited: bool = False
    wu_warning: bool = False
    wu_bailout: int = 0
    enemy_strength: float = 20.0  # Base health of enemies
    enemy_damage: float = 0.5    # Damage dealt by enemies 