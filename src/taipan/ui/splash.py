"""Splash screens for Taipan."""

from textual.app import ComposeResult
from textual.containers import Container, Center
from textual.screen import Screen
from textual.widgets import Static
from textual import events

class ShipSplash(Screen):
    """First splash screen showing the ship ASCII art."""
    
    BINDINGS = [("space", "next_screen", "Continue")]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Center(
            Container(
                Static("""
         _____  _    ___ ____   _    _   _
        |_   _|/ \\  |_ _|  _ \\ / \\  | \\ | |
          | | / _ \\  | || |_) / _ \\ |  \\| |
          | |/ ___ \\ | ||  __/ ___ \\| |\\  |
          |_/_/   \\_\\___|_| /_/   \\_\\_| \\_|

   A game based on the China trade of the 1800's

                      ~~|     ,
                       ,|`-._/|
                     .' |   /||\\
                   .'   | ./ ||`\\
                  / `-. |/._ ||  \\
                 /     `||  `|;-._\\
                 |      ||   ||   \\
~^~_-~^~=~^~~^= /       ||   ||__  \\~^=~^~-~^~_~^~=
 ~=~^~ _~^~ =~ `--------|`---||  `\"-`___~~^~ =_~^=
~ ~^~=~^_~^~ =~ \\~~~~~~~'~~~~'~~~~/~~`` ~=~^~ ~^=
 ~^=~^~_~-=~^~ ^ `--------------'~^~=~^~_~^=~^~=~
                """, id="ship-art"),
                Static("Press SPACE to continue", id="prompt"),
                id="splash-container"
            )
        )
    
    def action_next_screen(self) -> None:
        """Move to the credits screen."""
        self.app.push_screen("credits")
    
    CSS = """
    ShipSplash {
        background: $surface;
    }
    
    #splash-container {
        width: 60;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    
    #ship-art {
        text-align: center;
        color: $text;
    }
    
    #prompt {
        text-align: center;
        margin-top: 1;
        color: $text-muted;
    }
    """

class CreditsSplash(Screen):
    """Second splash screen showing credits."""
    
    BINDINGS = [("space", "next_screen", "Continue")]
    
    def compose(self) -> ComposeResult:
        """Create child widgets for the screen."""
        yield Center(
            Container(
                Static("""
                ===============
                 Created by:
                    Art Canfil
                ===============
                 Programmed by:
                    Jay Link
                   jlink@ilbbs.com
                ===============
                 Copyright (c)
                 1978 - 2002
                    Art Canfil
                ===============
                """, id="credits"),
                Static("Press SPACE to continue", id="prompt"),
                id="credits-container"
            )
        )
    
    def action_next_screen(self) -> None:
        """Move to the welcome screen."""
        self.app.push_screen("welcome")
    
    CSS = """
    CreditsSplash {
        background: $surface;
    }
    
    #credits-container {
        width: 40;
        height: auto;
        border: solid $accent;
        padding: 1;
    }
    
    #credits {
        text-align: center;
        color: $text;
    }
    
    #prompt {
        text-align: center;
        margin-top: 1;
        color: $text-muted;
    }
    """ 