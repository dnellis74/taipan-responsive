"""Main Textual application for Taipan."""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Header, Footer, Static

from ..models.game_engine import GameEngine
from .screens import WelcomeScreen, PortScreen, TradeScreen
from .splash import ShipSplash, CreditsSplash
from .widgets import StatusBar

class TaipanApp(App):
    """Main Taipan application."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    StatusBar {
        height: 1;
        width: 100%;
        layout: horizontal;
    }
    
    StatusBar Static {
        width: 25%;
        content-align: center middle;
    }
    """
    
    SCREENS = {
        "welcome": WelcomeScreen,
        "ship": ShipSplash,
        "credits": CreditsSplash,
        "port": PortScreen,
        "trade": TradeScreen,
    }
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.engine = None  # Will be initialized after welcome screen
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle app start-up."""
        # Start with the ship splash screen
        self.push_screen("ship")
    
    def update_status(self) -> None:
        """Update the status bar with current game state."""
        if self.engine is None:
            return
            
        player = self.engine.state.player
        status = self.query_one(StatusBar)
        
        status.query_one("#cash").update(f"Cash: {player.cash}")
        status.query_one("#cargo").update(
            f"Cargo: {sum(player.ship.hold.values())}/{player.ship.capacity}"
        )
        status.query_one("#guns").update(f"Guns: {player.ship.guns}")
        status.query_one("#location").update(
            f"Location: {self.engine.state.current_port.name.replace('_', ' ').title()}"
        )

    def on_ship_splash_complete(self) -> None:
        """Handle ship splash completion."""
        self.push_screen("credits")

    def on_credits_complete(self) -> None:
        """Handle credits completion."""
        self.push_screen("welcome")

    def on_welcome_complete(self, firm_name: str, starting_option: str) -> None:
        """Handle welcome completion."""
        # Create the game engine with the player's choices
        self.engine = GameEngine.new_game(firm_name, starting_option)
        
        # Update the status bar
        self.update_status()
        
        # Push the port screen
        self.push_screen("port")

    def on_key(self, event):
        """Handle key events."""
        if event.key == "?":
            self.show_help()
