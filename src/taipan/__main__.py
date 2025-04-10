"""Main entry point for Taipan."""

from .ui.app import TaipanApp

def main():
    """Run the Taipan game."""
    app = TaipanApp()
    app.run()

if __name__ == "__main__":
    main() 