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
    def new_game(cls, firm_name: str, starting_option: str) -> 'GameEngine':
        """Start a new game."""
        # Create player with initial state based on starting option
        player = Player()
        player.firm_name = firm_name
        
        if starting_option == "cash":
            player.cash = 1000
        elif starting_option == "guns":
            player.cash = 400
            player.ship.guns = 5
            player.ship.capacity = 10  # Each gun takes 10 units of cargo space
        
        # Initialize game state with the configured player
        state = GameState(player=player)
        return cls(state=state)
    
    def start_game(self, firm_name: str, initial_choice: str) -> None:
        """Initialize a new game with player's choices."""
        self.state.player.firm_name = firm_name
        
        # Initial setup based on player's choice
        if initial_choice.lower() == "cash":
            self.state.player.cash = 1000
            self.state.player.debt = 5000  # Start with debt if choosing cash
        else:  # guns
            self.state.player.ship.guns = 5
            self.state.player.cash = 400
            
        # No need to update prices as they are calculated dynamically
    
    def can_buy(self, commodity: Commodity, amount: int) -> Tuple[bool, str]:
        """Check if player can buy the specified amount."""
        price = self.state.current_port.get_price(commodity)
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
            
        price = self.state.current_port.get_price(commodity)
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
            
        price = self.state.current_port.get_price(commodity)
        total_value = price * amount
        
        self.state.player.cash += total_value
        self.state.player.ship.hold[commodity] -= amount
        return True
    
    def travel_to(self, destination: Port) -> None:
        """Travel to a new port."""
        if destination == self.state.current_port:
            return
            
        self.state.current_port = destination
        
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
        if self.state.current_port.name != "Hong Kong":
            return
            
        # Bank logic will be implemented here
        pass
    
    def handle_li_yuen(self) -> None:
        """Handle Li Yuen encounters in Hong Kong."""
        if (self.state.current_port.name == "Hong Kong" and 
            not self.state.li_yuen_visited and 
            self.state.player.cash > 0):
            # Li Yuen encounter logic will be implemented here
            self.state.li_yuen_visited = True 

    def buy_cargo(self, commodity: Commodity, amount: int) -> bool:
        """Buy cargo at current port."""
        port = self.state.current_port
        price = port.get_price(commodity)
        total_cost = price * amount

        if self.state.player.cash < total_cost:
            return False

        if not self.state.player.ship.can_load(amount):
            return False

        self.state.player.cash -= total_cost
        self.state.player.ship.load_cargo(commodity, amount)
        return True

    def sell_cargo(self, commodity: Commodity, amount: int) -> bool:
        """Sell cargo at current port."""
        if not self.state.player.ship.unload_cargo(commodity, amount):
            return False

        port = self.state.current_port
        price = port.get_price(commodity)
        total_value = price * amount

        self.state.player.cash += total_value
        return True

    def travel_to_port(self, port: Port) -> bool:
        """Travel to a new port."""
        if port == self.state.current_port:
            return False

        self.state.current_port = port
        self.state.advance_time(1)  # Travel takes 1 day
        return True

    def deposit_money(self, amount: int) -> bool:
        """Deposit money in bank."""
        return self.state.player.deposit(amount)

    def withdraw_money(self, amount: int) -> bool:
        """Withdraw money from bank."""
        return self.state.player.withdraw(amount)

    def borrow_money(self, amount: int) -> None:
        """Borrow money from Elder Brother Wu."""
        self.state.player.borrow(amount)

    def repay_debt(self, amount: int) -> None:
        """Repay debt to Elder Brother Wu."""
        self.state.player.repay(amount)

    def add_gun(self) -> bool:
        """Add a gun to the ship."""
        if self.state.player.cash < 1000:  # Cost of a gun
            return False
        self.state.player.cash -= 1000
        self.state.player.ship.add_gun()
        return True

    def remove_gun(self) -> bool:
        """Remove a gun from the ship."""
        if self.state.player.ship.guns == 0:
            return False
        self.state.player.ship.remove_gun()
        return True 