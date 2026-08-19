import shlex
import sys
import traceback
from config import VERSION
from engine.state import GameState
from engine.commands import COMMANDS
from engine.events import EventManager

class Game:
    def __init__(self):
        self.state = GameState()
        self.event_manager = EventManager()
        self.running = True

    def start(self):
        print(f"## ARCHIVE SYSTEM v{VERSION}")
        print("Authentication required.\n")
        
        while self.running:
            try:
                prompt = f"{self.state.current_dir}> "
                user_input = input(prompt).strip()
                
                if not user_input:
                    continue
                
                self.parse_input(user_input)
                
            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except Exception as e:
                print(f"CRITICAL ERROR: {e}")
                print(traceback.format_exc())

    def parse_input(self, text: str):
        try:
            parts = shlex.split(text)
        except ValueError as e:
            print(f"Syntax error: {e}")
            return
            
        cmd_name = parts[0].lower()
        args = parts[1:]
        
        self.state.stats["commands_entered"] += 1
        if cmd_name == self.state.stats.get("last_command"):
            self.state.stats["repeated_commands"] += 1
        else:
            self.state.stats["repeated_commands"] = 0
        self.state.stats["last_command"] = cmd_name
        
        self.event_manager.evaluate(self, action=cmd_name, target=" ".join(args))
        
        if cmd_name in COMMANDS:
            COMMANDS[cmd_name]["func"](self, args)
        else:
            from engine.terminal import slow_print
            slow_print(f"'{cmd_name}' is not recognized. It is watching your mistakes.", 0.02)
            self.event_manager.evaluate(self, action="failed_command", target=cmd_name)
