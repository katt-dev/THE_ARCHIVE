import sys
from engine.saves import save_game, load_game, delete_save
from engine.state import GameState

COMMANDS = {}

def command(name, aliases=None, hidden=False):
    def decorator(func):
        COMMANDS[name] = {"func": func, "hidden": hidden}
        if aliases:
            for alias in aliases:
                COMMANDS[alias] = {"func": func, "hidden": hidden}
        return func
    return decorator

@command("help", aliases=["?"])
def cmd_help(game, args):
    print("Available commands:")
    for cmd, data in COMMANDS.items():
        if not data["hidden"]:
            print(f"  {cmd}")

@command("pwd")
def cmd_pwd(game, args):
    print(game.state.current_dir)

@command("ls", aliases=["dir"])
def cmd_ls(game, args):
    items = game.state.fs.list_dir(game.state.current_dir)
    if not items:
        print("Directory is empty.")
    for item in items:
        prefix = "[DIR] " if item["data"]["type"] == "dir" else "[FILE]"
        if not item["data"]["metadata"].get("hidden", False):
            print(f"{prefix} {item['name']}")

@command("cd")
def cmd_cd(game, args):
    if not args:
        print("Usage: cd <path>")
        return
    
    target = args[0]
    new_path = game.state.fs.resolve_path(game.state.current_dir, target)
    
    node = game.state.fs.get_node(new_path)
    if node and node["type"] == "dir":
        game.state.current_dir = new_path
    else:
        print(f"Directory not found: {target}")

@command("cat", aliases=["open", "read"])
def cmd_cat(game, args):
    if not args:
        print("Usage: cat <filename>")
        return
        
    target = args[0]
    path = game.state.fs.resolve_path(game.state.current_dir, target)
    node = game.state.fs.get_node(path)
    
    if node and node["type"] == "file":
        if node.get("encrypted"):
            print("ERROR: File is encrypted. Use 'decrypt' command.")
        else:
            print(f"\n--- {target} ---")
            print(node.get("content", ""))
            print("-" * (len(target) + 8) + "\n")
            node["metadata"]["read"] = True
    else:
        print(f"File not found: {target}")

@command("save")
def cmd_save(game, args):
    slot = args[0] if args else "slot1"
    if save_game(game.state, slot):
        print(f"Game saved successfully to {slot}.")
    else:
        print("Failed to save game.")

@command("load")
def cmd_load(game, args):
    slot = args[0] if args else "slot1"
    new_state = load_game(slot)
    if new_state:
        game.state = new_state
        print(f"Game loaded successfully from {slot}.")
    else:
        print(f"Save slot '{slot}' not found.")

@command("reset")
def cmd_reset(game, args):
    confirm = input("WARNING: This will wipe current progress. Type 'YES' to confirm: ")
    if confirm == "YES":
        game.state = GameState()
        print("System reset. Memory wiped.")
    else:
        print("Reset aborted.")

@command("clear")
def cmd_clear(game, args):
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

@command("exit", aliases=["quit"])
def cmd_exit(game, args):
    print("Terminating connection...")
    game.running = False

# --- DEVELOPER / DEBUG COMMANDS ---
@command("debug", hidden=True)
def cmd_debug(game, args):
    if not args:
        print("Debug commands: state, flags, fs")
        return
    sub = args[0]
    if sub == "state":
        print(game.state.to_dict())
    elif sub == "flags":
        print(game.state.flags)
    elif sub == "fs":
        import json
        print(json.dumps(game.state.fs.nodes, indent=2))
    else:
        print("Unknown debug command.")
