from content.files import populate_filesystem
from content.horror_events import register_all_events
import content.custom_commands 

def load_content(game):
    if not game.state.flags.get("content_loaded"):
        populate_filesystem(game.state.fs)
        game.state.flags["content_loaded"] = True
    
    register_all_events(game)
