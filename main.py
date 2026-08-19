from engine.game import Game
from content.init import load_content
from content.personal_horror import run_pre_game_setup

if __name__ == "__main__":
    game = Game()
    
    if not game.state.flags.get("setup_complete"):
        run_pre_game_setup(game)
        game.state.flags["setup_complete"] = True
    
    load_content(game)
    
    game.start()
