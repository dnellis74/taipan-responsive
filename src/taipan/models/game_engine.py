"""Game engine for Taipan."""

import random
from dataclasses import dataclass
from typing import Optional, Tuple

from .game_state import GameState, Port, Commodity, Player, Ship

@dataclass
class GameEngine:
    """Handles core game logic and state transitions."""
    
    state: GameState
    
    @classmethod
    def new_game(cls) -> 'GameEngine':
        """Create a new game with initial state."""
        return cls(GameState())
    
    def start_game(self, firm_name: str, initial_choice: str) -> None:
        """Initialize a new game with player's choices."""
        self.state.player.firm_name = firm_name
        
        # Initial setup based on player's choice
        if initial_choice.lower() == "cash":
            self.state.player.cash = 1000
        else:  # guns
            self.state.player.ship.guns = 5
            self.state.player.cash = 400
            
        self._update_prices()
    
    def _update_prices(self) -> None:
        """Update market prices based on port and random factors."""
        for commodity in Commodity:
            base = self.state.market.base_prices[commodity][self.state.current_port]
            for port in Port:
                if port == Port.AT_SEA:
                    continue
                # Prices vary by ±30% from base
                variation = random.uniform(0.7, 1.3)
                self.state.market.prices[commodity][port] = int(
                    base * variation * self.state.market.base_prices[commodity][port]
                )
    
    def can_buy(self, commodity: Commodity, amount: int) -> Tuple[bool, str]:
        """Check if player can buy the specified amount."""
        price = self.state.market.prices[commodity][self.state.current_port]
        total_cost = price * amount
        
        if total_cost > self.state.player.cash:
            return False, "Not enough cash"
            
        current_hold = sum(self.state.player.ship.hold.values())
        if current_hold + amount > self.state.player.ship.capacity:
            return False, "Not enough cargo space"
            
        return True, ""
    
    def buy(self, commodity: Commodity, amount: int) -> bool:
        """Attempt to buy commodity."""
        can_buy, reason = self.can_buy(commodity, amount)
        if not can_buy:
            return False
            
        price = self.state.market.prices[commodity][self.state.current_port]
        total_cost = price * amount
        
        self.state.player.cash -= total_cost
        self.state.player.ship.hold[commodity] += amount
        return True
    
    def can_sell(self, commodity: Commodity, amount: int) -> Tuple[bool, str]:
        """Check if player can sell the specified amount."""
        if amount > self.state.player.ship.hold[commodity]:
            return False, "Not enough cargo"
        return True, ""
    
    def sell(self, commodity: Commodity, amount: int) -> bool:
        """Attempt to sell commodity."""
        can_sell, reason = self.can_sell(commodity, amount)
        if not can_sell:
            return False
            
        price = self.state.market.prices[commodity][self.state.current_port]
        total_value = price * amount
        
        self.state.player.cash += total_value
        self.state.player.ship.hold[commodity] -= amount
        return True
    
    def travel_to(self, destination: Port) -> None:
        """Travel to a new port."""
        if destination == self.state.current_port:
            return
            
        self.state.current_port = destination
        self._update_prices()
        
        # Advance time
        self.state.month += 1
        if self.state.month > 12:
            self.state.month = 1
            self.state.year += 1
            
        # Increase difficulty over time
        self.state.enemy_strength *= 1.05
        self.state.enemy_damage *= 1.02
    
    def visit_bank(self) -> None:
        """Handle bank interactions in Hong Kong."""
        if self.state.current_port != Port.HONG_KONG:
            return
            
        # Bank logic will be implemented here
        pass
    
    def handle_li_yuen(self) -> None:
        """Handle Li Yuen encounters in Hong Kong."""
        if (self.state.current_port == Port.HONG_KONG and 
            not self.state.li_yuen_visited and 
            self.state.player.cash > 0):
            # Li Yuen encounter logic will be implemented here
            self.state.li_yuen_visited = True 