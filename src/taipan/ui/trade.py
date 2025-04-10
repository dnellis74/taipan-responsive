"""Trade screen for Taipan."""

from typing import Dict, List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Input, Static

from taipan.models.game_state import GameState


class TradeScreen(Screen):
    """Screen for trading cargo."""

    CSS = """
    Screen {
        align: center middle;
    }

    #trade-container {
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

    Input {
        width: 100%;
        margin: 1;
    }

    .highlight {
        background: $accent;
        color: $text;
    }
    """

    def __init__(self, game_state: GameState) -> None:
        """Initialize the trade screen."""
        super().__init__()
        self.game_state = game_state
        self.current_port = game_state.current_port
        self.selected_cargo: Optional[str] = None
        self.trade_amount = 0

    def compose(self) -> ComposeResult:
        """Compose the trade screen."""
        yield Header()
        with Container(id="trade-container"):
            yield Static(self._render_status(), id="status-panel")
            yield Static(self._render_cargo(), id="cargo-panel")
            with Vertical(id="actions-panel"):
                yield Input(placeholder="Enter amount to trade", id="amount-input")
                yield Button("Buy", id="buy-button")
                yield Button("Sell", id="sell-button")
                yield Button("Back", id="back-button")

    def _render_status(self) -> RenderableType:
        """Render the status panel."""
        table = Table(show_header=False, box=None)
        table.add_column("Label", style="bold")
        table.add_column("Value")

        table.add_row("Cash", f"${self.game_state.player.cash:,}")
        table.add_row("Cargo Space", f"{self.game_state.ship.used_cargo_space}/{self.game_state.ship.max_cargo_space}")
        if self.selected_cargo:
            price = self.current_port.cargo_prices[self.selected_cargo]
            table.add_row("Selected Cargo", f"{self.selected_cargo} (${price:,})")

        return Panel(table, title="Status")

    def _render_cargo(self) -> RenderableType:
        """Render the cargo panel."""
        table = Table(show_header=True, box=None)
        table.add_column("Cargo")
        table.add_column("Price", justify="right")
        table.add_column("Your Cargo", justify="right")

        for cargo in self.current_port.available_cargo:
            price = self.current_port.cargo_prices[cargo]
            player_cargo = self.game_state.ship.cargo.get(cargo, 0)
            
            row_style = "highlight" if cargo == self.selected_cargo else ""
            table.add_row(
                cargo,
                f"${price:,}",
                str(player_cargo),
                style=row_style
            )

        return Panel(table, title="Cargo Market")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Handle input changes."""
        if event.input.id == "amount-input":
            try:
                self.trade_amount = int(event.value)
            except ValueError:
                self.trade_amount = 0

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        if button_id == "buy-button":
            self._buy_cargo()
        elif button_id == "sell-button":
            self._sell_cargo()
        elif button_id == "back-button":
            self.app.pop_screen()

    def _buy_cargo(self) -> None:
        """Buy cargo."""
        if not self.selected_cargo or self.trade_amount <= 0:
            self.notify("Select cargo and enter amount to buy!")
            return

        price = self.current_port.cargo_prices[self.selected_cargo]
        total_cost = price * self.trade_amount
        available_space = self.game_state.ship.max_cargo_space - self.game_state.ship.used_cargo_space

        if self.trade_amount > available_space:
            self.notify(f"Not enough cargo space! Available: {available_space}")
            return

        if self.game_state.player.cash < total_cost:
            self.notify(f"Not enough cash! Need ${total_cost:,}")
            return

        # Complete the transaction
        self.game_state.player.cash -= total_cost
        self.game_state.ship.cargo[self.selected_cargo] = self.game_state.ship.cargo.get(self.selected_cargo, 0) + self.trade_amount
        self.game_state.ship.used_cargo_space += self.trade_amount

        self.notify(f"Bought {self.trade_amount} {self.selected_cargo} for ${total_cost:,}")
        self.refresh()

    def _sell_cargo(self) -> None:
        """Sell cargo."""
        if not self.selected_cargo or self.trade_amount <= 0:
            self.notify("Select cargo and enter amount to sell!")
            return

        price = self.current_port.cargo_prices[self.selected_cargo]
        total_value = price * self.trade_amount
        player_cargo = self.game_state.ship.cargo.get(self.selected_cargo, 0)

        if player_cargo < self.trade_amount:
            self.notify(f"Not enough cargo to sell! You have {player_cargo}")
            return

        # Complete the transaction
        self.game_state.player.cash += total_value
        self.game_state.ship.cargo[self.selected_cargo] -= self.trade_amount
        if self.game_state.ship.cargo[self.selected_cargo] == 0:
            del self.game_state.ship.cargo[self.selected_cargo]
        self.game_state.ship.used_cargo_space -= self.trade_amount

        self.notify(f"Sold {self.trade_amount} {self.selected_cargo} for ${total_value:,}")
        self.refresh()

    def on_key(self, event) -> None:
        """Handle key presses."""
        if event.key == "escape":
            self.app.pop_screen() 