"""Game screens for Taipan."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Input, Label, Static

from taipan.ui.widgets import StatusBar

class BaseGameScreen(Screen):
    """Base game screen with status bar."""
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield StatusBar()
        yield Container(
            Vertical(
                id="screen-content"
            )
        )
    
    CSS = """
    BaseGameScreen {
        align: center middle;
    }
    
    #screen-content {
        width: 40;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    """

class WelcomeScreen(BaseGameScreen):
    """Welcome screen with game setup."""
    
    BINDINGS = [("escape", "app.quit", "Quit")]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield from super().compose()
        yield Container(
            Vertical(
                Static("Welcome to Taipan!", id="title"),
                Static("A trading game set in the Far East", id="subtitle"),
                Label("Enter your firm's name:"),
                Input(placeholder="Firm name", id="firm-name"),
                Static("\nStart with:"),
                Button("1000 Cash", id="cash", variant="primary"),
                Button("5 Guns and 400 Cash", id="guns", variant="primary"),
                id="welcome-dialog"
            )
        )
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        firm_name = self.query_one("#firm-name").value
        if not firm_name:
            self.query_one("#firm-name").focus()
            return
            
        # Get the starting option from the button ID
        starting_option = event.button.id
        
        # Notify the app that welcome is complete with the firm name and starting option
        self.app.on_welcome_complete(firm_name, starting_option)
        self.app.pop_screen()
    
    CSS = """
    WelcomeScreen {
        align: center middle;
    }
    
    #welcome-dialog {
        width: 40;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    
    #title {
        text-align: center;
        text-style: bold;
    }
    
    #subtitle {
        text-align: center;
        margin-bottom: 1;
    }
    
    Button {
        margin: 1 0;
        width: 100%;
    }
    """

class PortScreen(BaseGameScreen):
    """Main port interface screen."""
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield from super().compose()
        yield Container(
            Vertical(
                Static("Port Actions", id="title"),
                Button("Buy Goods", id="buy"),
                Button("Sell Goods", id="sell"),
                Button("Visit Bank", id="bank"),
                Button("Set Sail", id="sail"),
                id="port-actions"
            )
        )
    
    CSS = """
    PortScreen {
        align: center middle;
    }
    
    #port-actions {
        width: 30;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    
    Button {
        margin: 1 0;
        width: 100%;
    }
    """

class TradeScreen(BaseGameScreen):
    """Trading interface screen."""
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield from super().compose()
        yield Container(
            Vertical(
                Static("Trade", id="title"),
                # We'll add the trading interface later
                id="trade-interface"
            )
        )
    
    CSS = """
    TradeScreen {
        align: center middle;
    }
    
    #trade-interface {
        width: 40;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    """ 