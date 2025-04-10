"""Ship model for Taipan."""

from dataclasses import dataclass, field
from typing import Dict

from taipan.models.commodity import Commodity

@dataclass
class Ship:
    """Player's ship status."""
    capacity: int = 60
    damage: int = 0
    guns: int = 0
    hold: Dict[Commodity, int] = field(
        default_factory=lambda: {c: 0 for c in Commodity}
    )

    def get_total_cargo(self) -> int:
        """Get total amount of cargo in hold."""
        return sum(self.hold.values())

    def get_available_space(self) -> int:
        """Get available cargo space."""
        return self.capacity - self.get_total_cargo()

    def can_load(self, amount: int) -> bool:
        """Check if ship can load specified amount of cargo."""
        return self.get_available_space() >= amount

    def load_cargo(self, commodity: Commodity, amount: int) -> bool:
        """Load cargo onto ship if space available."""
        if self.can_load(amount):
            self.hold[commodity] += amount
            return True
        return False

    def unload_cargo(self, commodity: Commodity, amount: int) -> bool:
        """Unload cargo from ship if available."""
        if self.hold[commodity] >= amount:
            self.hold[commodity] -= amount
            return True
        return False

    def get_status(self) -> str:
        """Get ship's status description."""
        status = 100 - ((self.damage / self.capacity) * 100)
        if status <= 0:
            return "Critical"
        elif status <= 20:
            return "Poor"
        elif status <= 40:
            return "Fair"
        elif status <= 60:
            return "Good"
        elif status <= 80:
            return "Prime"
        else:
            return "Perfect"

    def repair(self, amount: int) -> None:
        """Repair ship damage."""
        self.damage -= amount
        if self.damage < 0:
            self.damage = 0

    def add_gun(self) -> None:
        """Add a gun to the ship."""
        self.guns += 1
        self.capacity -= 10  # Each gun takes 10 units of cargo space

    def remove_gun(self) -> None:
        """Remove a gun from the ship."""
        if self.guns > 0:
            self.guns -= 1
            self.capacity += 10  # Recover 10 units of cargo space 