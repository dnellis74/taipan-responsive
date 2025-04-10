"""Port screen for Taipan."""

from typing import Dict, List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Static

from taipan.models.game_state import GameState
from taipan.models.port import Port
from taipan.models.ship import Ship


class PortScreen(Screen):
    """Screen for port operations."""

    CSS = """
    Screen {
        align: center middle;
    }

    #port-container {
        width: 80%;
        height: 80%;
        border: solid $accent;
    }

    #status-panel {
        width: 100%;
        height: 20%;
        border: solid $accent;
        padding: 1;
    }

    #cargo-panel {
        width: 100%;
        height: 40%;
        border: solid $accent;
        padding: 1;
    }

    #actions-panel {
        width: 100%;
        height: 20%;
        border: solid $accent;
        padding: 1;
    }

    Button {
        width: 100%;
        margin: 1;
    }

    .highlight {
        background: $accent;
        color: $text;
    }
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize the port screen."""
        super().__init__()
        self.game_state = game_state
        self.current_port = game_state.current_port
        self.selected_cargo: Optional[str] = None
        self.trade_amount = 0

    def compose(self) -> ComposeResult:
        """Compose the port screen."""
        yield Header()
        with Container(id="port-container"):
            yield Static(self._render_status(), id="status-panel")
            yield Static(self._render_cargo(), id="cargo-panel")
            with Vertical(id="actions-panel"):
                yield Button("Trade", id="trade-button")
                yield Button("Repair Ship", id="repair-button")
                yield Button("Pay Debt", id="debt-button")
                yield Button("Travel", id="travel-button")

    def _render_status(self) -> RenderableType:
        """Render the status panel."""
        table = Table(show_header=False, box=None)
        table.add_column("Label", style="bold")
        table.add_column("Value")

        table.add_row("Port", self.current_port.name)
        table.add_row("Cash", f"${self.game_state.player.cash:,}")
        table.add_row("Debt", f"${self.game_state.player.debt:,}")
        table.add_row("Ship Condition", f"{self.game_state.ship.condition}%")
        table.add_row("Cargo Space", f"{self.game_state.ship.used_cargo_space}/{self.game_state.ship.max_cargo_space}")

        return Panel(table, title="Status")

    def _render_cargo(self) -> RenderableType:
        """Render the cargo panel."""
        table = Table(show_header=True, box=None)
        table.add_column("Cargo")
        table.add_column("Price", justify="right")
        table.add_column("Available", justify="right")
        table.add_column("Your Cargo", justify="right")

        for cargo in self.current_port.available_cargo:
            price = self.current_port.cargo_prices[cargo]
            available = self.current_port.cargo_quantities[cargo]
            player_cargo = self.game_state.ship.cargo.get(cargo, 0)
            
            row_style = "highlight" if cargo == self.selected_cargo else ""
            table.add_row(
                cargo,
                f"${price:,}",
                str(available),
                str(player_cargo),
                style=row_style
            )

        return Panel(table, title="Cargo Market")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        if button_id == "trade-button":
            self.app.push_screen("trade")
        elif button_id == "repair-button":
            self._repair_ship()
        elif button_id == "debt-button":
            self._pay_debt()
        elif button_id == "travel-button":
            self.app.push_screen("travel")

    def _repair_ship(self) -> None:
        """Repair the ship."""
        cost = (100 - self.game_state.ship.condition) * 10
        if self.game_state.player.cash >= cost:
            self.game_state.player.cash -= cost
            self.game_state.ship.condition = 100
            self.notify(f"Ship repaired for ${cost:,}")
        else:
            self.notify("Not enough cash to repair ship!")

    def _pay_debt(self) -> None:
        """Pay off debt."""
        if self.game_state.player.debt > 0:
            amount = min(self.game_state.player.cash, self.game_state.player.debt)
            self.game_state.player.cash -= amount
            self.game_state.player.debt -= amount
            self.notify(f"Paid ${amount:,} towards debt")
        else:
            self.notify("You have no debt to pay!")

    def on_key(self, event) -> None:
        """Handle key presses."""
        if event.key == "escape":
            self.app.pop_screen() 