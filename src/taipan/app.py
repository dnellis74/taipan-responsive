"""Main Textual application for Taipan!"""

from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer

class TaipanApp(App):
    """Main application class for Taipan!"""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    Container {
        width: 54;
        height: 18;
        border: solid $accent;
    }
    """
    
    def compose(self) -> ComposeResult:
        """Compose the app layout."""
        yield Header()
        yield Container()
        yield Footer()

def main():
    """Run the Taipan! application."""
    app = TaipanApp()
    app.run()

if __name__ == "__main__":
    main() 