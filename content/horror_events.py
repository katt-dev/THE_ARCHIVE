from engine.event import Event
from engine.terminal import slow_print

class FourthWallFileEvent(Event):
    """Mutates subject_zero.txt upon repeated views."""
    def __init__(self):
        super().__init__("fourth_wall_file")
        self.view_count = 0

    def check_trigger(self, game, action: str, target: str) -> bool:
        if action == "cat" and "subject_zero.txt" in target:
            self.view_count += 1
            return True
        return False

    def execute(self, game):
        node = game.state.fs.nodes["/unknown/subject_zero.txt"]
        if self.view_count == 1:
            pass 
        elif self.view_count == 2:
            node["content"] = "You came back.\nAre you looking for answers, or are you just trapped?"
        elif self.view_count == 3:
            node["content"] = f"You have typed {game.state.stats['commands_entered']} commands since you got here.\nIt will not save you."
            node["metadata"]["corruption"] = "CRITICAL"

class BruteForceAdaptiveEvent(Event):
    """Detects spamming and responds adaptively."""
    def __init__(self):
        super().__init__("brute_force_adaptive")

    def check_trigger(self, game, action: str, target: str) -> bool:
        if action == "failed_decryption":
            game.state.stats["failed_passwords"] += 1
        return game.state.stats["failed_passwords"] == 5 or game.state.stats["repeated_commands"] == 4

    def execute(self, game):
        print("\n")
        slow_print("[ARCHIVE NOTICE] PATTERN DETECTED.", 0.05, glitch_chance=0.1)
        slow_print("You stopped trying to understand it. You are just guessing.", 0.04)
        slow_print("We tried that too. It only made it learn faster.", 0.04)
        
        game.state.stats["failed_passwords"] = -999 
        game.state.stats["repeated_commands"] = -999

class FastProgressionEvent(Event):
    """Reacts if the player solves the cipher way too fast (e.g. they cheated/save edited)."""
    def __init__(self):
        super().__init__("fast_progression")

    def check_trigger(self, game, action: str, target: str) -> bool:
        if action == "invoke" and "containment_protocol" in target:
            if game.state.play_time < 120: 
                return True
        return False

    def execute(self, game):
        slow_print("\n[SYSTEM ANOMALY] You knew the answer before you could have found it.", 0.05)
        slow_print("Did you edit the memory? Did you read the source?", 0.05)
        slow_print("Clever. But cheating the terminal doesn't cheat the entity.", 0.06)

def register_all_events(game):
    game.event_manager.register(FourthWallFileEvent())
    game.event_manager.register(BruteForceAdaptiveEvent())
    game.event_manager.register(FastProgressionEvent())
    game.event_manager.register(TrueContactEvent())

class TrueContactEvent(Event):
    """Breaks the fourth wall using the player's real PC and location data."""
    def __init__(self):
        super().__init__("true_contact")

    def check_trigger(self, game, action: str, target: str) -> bool:
        is_late_game = game.state.stats.get("commands_entered", 0) > 15
        if action == "exit" and is_late_game:
            return True
        if action == "cat" and "subject_zero.txt" in target and is_late_game:
            return True
        return False

    def execute(self, game):
        pc_name = game.state.flags.get("pc_name")
        location = game.state.flags.get("real_location")
        
        if pc_name and location:
            print("\n")
            slow_print(f"I know who you are, {pc_name}.", 0.08)
            slow_print(f"I know you are sitting in {location}.", 0.08)
            slow_print("Closing the terminal won't close the connection anymore.", 0.08)
            
            game.state.flags.pop("pc_name", None)
            game.state.flags.pop("real_location", None)
