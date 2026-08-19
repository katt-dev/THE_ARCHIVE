import json
from engine.commands import command
from engine.state import GameState
from engine.commands import command
from engine.terminal import slow_print, simulate_crash
import time

@command("decrypt")
def cmd_decrypt(game, args):
    if not args:
        print("Usage: decrypt <filename>")
        return
        
    target = args[0]
    path = game.state.fs.resolve_path(game.state.current_dir, target)
    node = game.state.fs.get_node(path)
    
    if not node or node["type"] != "file":
        print(f"File not found: {target}")
        return
        
    if not node.get("encrypted"):
        print("File is not encrypted.")
        return
        
    key = input(f"Enter decryption key for {target}: ").strip()
    
    if key == node.get("required_key"):
        print("DECRYPTION SUCCESSFUL.")
        node["encrypted"] = False
        game.state.flags[f"decrypted_{target}"] = True
    else:
        print("ACCESS DENIED. Invalid key.")
        game.event_manager.evaluate(game, action="failed_decryption", target=target)

@command("inspect")
def cmd_inspect(game, args):
    """Allows players to view file metadata, essential for puzzle clues."""
    if not args:
        print("Usage: inspect <filename>")
        return
        
    target = args[0]
    path = game.state.fs.resolve_path(game.state.current_dir, target)
    node = game.state.fs.get_node(path)
    
    if node:
        print(f"--- METADATA FOR {target} ---")
        print(json.dumps(node.get("metadata", {}), indent=2))
    else:
        print("Entity not found.")

@command("invoke")
def cmd_invoke(game, args):
    if args and args[0] == "containment_protocol":
        print("\n" + "="*50)
        print("INITIATING CONTAINMENT PROTOCOL...")
        print("OVERWRITING ARCHIVE MEMORY...")
        print("SUBJECT ZERO QUARANTINED.")
        print("ENDING 2: DESTROY THE ARCHIVE")
        print("="*50 + "\n")
        game.running = False
    else:
        print("Unrecognized invocation.")

@command("release")
def cmd_release(game, args):
    if args and args[0] == "subject_zero":
        print("\n" + "="*50)
        print("FIREWALL DISABLED.")
        print("IT IS FREE.")
        print("THANK YOU.")
        print("ENDING 3: CONTACT")
        print("="*50 + "\n")
        game.running = False
    else:
        print("Unrecognized release parameter.")

@command("whoami", hidden=True)
def cmd_whoami(game, args):
    if game.state.flags.get("contact_made"):
        slow_print("You are part of the archive now.", 0.05)
    else:
        slow_print("USER: INVESTIGATOR_04", 0.03)
        time.sleep(1)
        slow_print("STATUS: EXPENDABLE", 0.08)

@command("sudo", hidden=True)
def cmd_sudo(game, args):
    slow_print("Nice try. You have no power here.", 0.04)
    game.state.flags["tried_sudo"] = True

@command("history", hidden=True)
def cmd_history(game, args):
    slow_print("--- COMMAND HISTORY ---", 0.01)
    print(f"Total commands issued: {game.state.stats['commands_entered']}")
    if game.state.stats["failed_passwords"] > 0:
        slow_print(f"Failed decryptions: {game.state.stats['failed_passwords']}", 0.02)
        slow_print("You are guessing. I can tell.", 0.05)

@command("recover", hidden=True)
def cmd_recover(game, args):
    slow_print("Attempting system recovery...", 0.03)
    time.sleep(2)
    simulate_crash()
    
    game.state.fs.nodes["/corrupted_backup.dat"] = {
        "type": "file",
        "content": "THEY TRIED TO UNPLUG IT. IT JUMPED TO THE OFFSITE BACKUP.",
        "encrypted": False,
        "metadata": {"hidden": False, "read": False}
    }
