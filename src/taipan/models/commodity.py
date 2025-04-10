"""Commodity model for Taipan."""

from enum import Enum, auto

class Commodity(Enum):
    """Tradeable commodities in Taipan."""
    OPIUM = auto()
    SILK = auto()
    ARMS = auto()
    GENERAL = auto()

    @classmethod
    def from_string(cls, name: str) -> 'Commodity':
        """Convert string name to Commodity enum."""
        name = name.upper().replace(' ', '_')
        if name == 'GENERAL_CARGO':
            name = 'GENERAL'
        return cls[name]

    def __str__(self) -> str:
        """Convert Commodity enum to display string."""
        if self == Commodity.GENERAL:
            return "General Cargo"
        return self.name.capitalize()

    @staticmethod
    def get_base_price(commodity: 'Commodity', port_index: int) -> int:
        """Get base price for this commodity at given port index.
        
        Based on the original C code's base_price array:
        int base_price[4][8] = { 
            {1000, 11, 16, 15, 14, 12, 10, 13},  // Opium
            {100,  11, 14, 15, 16, 10, 13, 12},  // Silk
            {10,   12, 16, 10, 11, 13, 14, 15},  // Arms
            {1,    10, 11, 12, 13, 14, 15, 16}   // General Cargo
        };
        """
        base_prices = {
            Commodity.OPIUM: [1000, 11, 16, 15, 14, 12, 10, 13],
            Commodity.SILK: [100, 11, 14, 15, 16, 10, 13, 12],
            Commodity.ARMS: [10, 12, 16, 10, 11, 13, 14, 15],
            Commodity.GENERAL: [1, 10, 11, 12, 13, 14, 15, 16]
        }
        return base_prices[commodity][port_index]

    def get_short_name(self) -> str:
        """Get short name for the commodity (used in menus)."""
        if self == Commodity.GENERAL:
            return "General"
        return self.name.capitalize()

    def get_letter(self) -> str:
        """Get the letter used to select this commodity in menus."""
        if self == Commodity.GENERAL:
            return "G"
        return self.name[0] 