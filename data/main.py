"""
The main function is defined here. It simply creates an instance of
tools.Control and adds the game states to its dictionary using
tools.setup_states.  There should be no need (theoretically) to edit
the tools.Control class.  All modifications should occur in this module
and in the prepare module.
"""

from . import prepare, tools
from .states import splash, intro, game, overworld, battle, town, menu


def main():
    """Add states to control here."""
    run_it = tools.Control(prepare.ORIGINAL_CAPTION)
    state_dict = {  "SPLASH" : splash.Splash(),
                    "INTRO"  : intro.Intro(),
                    "GAME"   : game.Game(),

                    "OVERWORLD": overworld.Overworld(),
                    "BATTLE": battle.Battle(),
                    "TOWN": town.Town(),
                    "MENU": menu.Menu(),
    }
    run_it.setup_states(state_dict, "OVERWORLD")
    run_it.main()
