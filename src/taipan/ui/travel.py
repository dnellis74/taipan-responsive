"""Travel screen for Taipan."""

from typing import Dict, List, Optional

from rich.console import RenderableType
from rich.panel import Panel
from rich.table import Table
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Header, Static

from taipan.models.game_state import GameState
from taipan.models.port import Port


class TravelScreen(Screen):
    """Screen for traveling between ports."""

    CSS = """
    Screen {
        align: center middle;
    }

    #travel-container {
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

    #ports-panel {
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
        """Initialize the travel screen."""
        super().__init__()
        self.game_state = game_state
        self.current_port = game_state.current_port
        self.selected_port: Optional[Port] = None

    def compose(self) -> ComposeResult:
        """Compose the travel screen."""
        yield Header()
        with Container(id="travel-container"):
            yield Static(self._render_status(), id="status-panel")
            yield Static(self._render_ports(), id="ports-panel")
            with Vertical(id="actions-panel"):
                yield Button("Travel", id="travel-button")
                yield Button("Back", id="back-button")

    def _render_status(self) -> RenderableType:
        """Render the status panel."""
        table = Table(show_header=False, box=None)
        table.add_column("Label", style="bold")
        table.add_column("Value")

        table.add_row("Current Port", self.current_port.name)
        table.add_row("Ship Condition", f"{self.game_state.ship.condition}%")
        if self.selected_port:
            distance = self.current_port.distance_to(self.selected_port)
            table.add_row("Distance", f"{distance} miles")
            table.add_row("Fuel Cost", f"${distance * 10:,}")

        return Panel(table, title="Status")

    def _render_ports(self) -> RenderableType:
        """Render the ports panel."""
        table = Table(show_header=True, box=None)
        table.add_column("Port")
        table.add_column("Distance", justify="right")
        table.add_column("Fuel Cost", justify="right")

        for port in self.game_state.ports:
            if port != self.current_port:
                distance = self.current_port.distance_to(port)
                fuel_cost = distance * 10
                row_style = "highlight" if port == self.selected_port else ""
                table.add_row(
                    port.name,
                    f"{distance} miles",
                    f"${fuel_cost:,}",
                    style=row_style
                )

        return Panel(table, title="Available Ports")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        if button_id == "travel-button":
            self._travel_to_port()
        elif button_id == "back-button":
            self.app.pop_screen()

    def _travel_to_port(self) -> None:
        """Travel to the selected port."""
        if not self.selected_port:
            self.notify("Select a port to travel to!")
            return

        distance = self.current_port.distance_to(self.selected_port)
        fuel_cost = distance * 10

        if self.game_state.player.cash < fuel_cost:
            self.notify(f"Not enough cash for fuel! Need ${fuel_cost:,}")
            return

        # Deduct fuel cost and update current port
        self.game_state.player.cash -= fuel_cost
        self.game_state.current_port = self.selected_port

        # Update ship condition (random damage during travel)
        damage = self.game_state.random.randint(1, 5)
        self.game_state.ship.condition = max(0, self.game_state.ship.condition - damage)

        self.notify(f"Traveled to {self.selected_port.name} for ${fuel_cost:,}")
        self.app.pop_screen()  # Return to port screen

    def on_key(self, event) -> None:
        """Handle key presses."""
        if event.key == "escape":
            self.app.pop_screen() 