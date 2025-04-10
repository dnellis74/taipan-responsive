"""Main Textual application for Taipan."""

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive

from ..models.game_engine import GameEngine
from ..models.game_state import Port, Commodity
from .screens import WelcomeScreen, PortScreen, TradeScreen

class StatusBar(Static):
    """Status bar showing player's current status."""
    
    def compose(self) -> ComposeResult:
        """Compose the status bar."""
        yield Static("Cash: 0", id="cash")
        yield Static("Cargo: 0/60", id="cargo")
        yield Static("Guns: 0", id="guns")
        yield Static("Location: Hong Kong", id="location")

class GameScreen(Container):
    """Main game screen."""
    
    def compose(self) -> ComposeResult:
        """Compose the game screen."""
        yield Vertical(
            StatusBar(),
            Container(
                id="main-content"
            ),
            Container(
                id="message-area"
            ),
        )

class TaipanApp(App):
    """Main Taipan application."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    GameScreen {
        width: 54;
        height: 18;
        border: solid $accent;
        padding: 1;
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
    
    #main-content {
        height: 12;
    }
    
    #message-area {
        height: 3;
        border-top: solid $accent;
    }
    """
    
    SCREENS = {
        "welcome": WelcomeScreen(),
        "port": PortScreen(),
        "trade": TradeScreen(),
    }
    
    def __init__(self):
        """Initialize the application."""
        super().__init__()
        self.engine = GameEngine.new_game()
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield GameScreen()
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle app start-up."""
        # Start new game setup
        self.push_screen("welcome")
    
    def update_status(self) -> None:
        """Update the status bar with current game state."""
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