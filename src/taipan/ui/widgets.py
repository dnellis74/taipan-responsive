"""Custom widgets for Taipan."""

from textual.widgets import Static
from textual.app import ComposeResult

class StatusBar(Static):
    """Status bar showing player's current status."""
    
    def compose(self) -> ComposeResult:
        """Compose the status bar."""
        yield Static("Cash: 0", id="cash")
        yield Static("Cargo: 0/60", id="cargo")
        yield Static("Guns: 0", id="guns")
        yield Static("Location: Hong Kong", id="location") 