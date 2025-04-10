"""Player model for Taipan."""

from dataclasses import dataclass, field
from typing import Dict

from taipan.models.commodity import Commodity
from taipan.models.ship import Ship

@dataclass
class Player:
    """Player's status including finances and firm name."""
    firm_name: str = ""
    cash: int = 0
    bank: int = 0
    debt: int = 0
    warehouse: Dict[Commodity, int] = field(
        default_factory=lambda: {c: 0 for c in Commodity}
    )
    hold: Dict[Commodity, int] = field(
        default_factory=lambda: {c: 0 for c in Commodity}
    )
    ship: Ship = field(default_factory=lambda: Ship(capacity=60))
    month: int = 1
    year: int = 1860
    li_yuen_visited: bool = False
    wu_warning: bool = False
    wu_bailout: int = 0
    enemy_strength: float = 20.0  # Base health of enemies
    enemy_damage: float = 0.5    # Damage dealt by enemies

    def get_total_cargo(self) -> int:
        """Get total amount of cargo in hold."""
        return self.ship.get_total_cargo()

    def get_warehouse_used(self) -> int:
        """Get amount of warehouse space used."""
        return sum(self.warehouse.values())

    def get_warehouse_available(self) -> int:
        """Get amount of warehouse space available."""
        return 10000 - self.get_warehouse_used()

    def can_afford(self, amount: int) -> bool:
        """Check if player can afford an amount."""
        return self.cash >= amount

    def pay(self, amount: int) -> bool:
        """Pay an amount from cash if possible."""
        if self.can_afford(amount):
            self.cash -= amount
            return True
        return False

    def deposit(self, amount: int) -> bool:
        """Deposit money from cash to bank."""
        if self.can_afford(amount):
            self.cash -= amount
            self.bank += amount
            return True
        return False

    def withdraw(self, amount: int) -> bool:
        """Withdraw money from bank to cash."""
        if self.bank >= amount:
            self.bank -= amount
            self.cash += amount
            return True
        return False

    def borrow(self, amount: int) -> None:
        """Borrow money from Elder Brother Wu."""
        self.cash += amount
        self.debt += amount

    def repay(self, amount: int) -> None:
        """Repay debt to Elder Brother Wu."""
        if self.cash >= amount:
            self.cash -= amount
            self.debt -= amount
            if self.debt < 0:
                self.debt = 0

    def get_net_worth(self) -> int:
        """Calculate player's total net worth."""
        return self.cash + self.bank - self.debt 