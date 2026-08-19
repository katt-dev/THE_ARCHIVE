class Puzzle:
    """Base class for all puzzles."""
    def __init__(self, puzzle_id: str, name: str, description: str):
        self.id = puzzle_id
        self.name = name
        self.description = description
        self.solved = False

    def check_conditions(self, state) -> bool:
        """Override to check if puzzle can be interacted with."""
        return True

    def validate_input(self, user_input: str, state) -> bool:
        """Override to validate the solution."""
        return False

    def on_success(self, game):
        """Override to define rewards/changes."""
        self.solved = True
        game.state.flags[f"puzzle_{self.id}_solved"] = True

    def on_failure(self, game):
        """Override to define consequences of failure."""
        pass
