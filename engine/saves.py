import json
import os
from config import SAVE_DIR, SAVE_VERSION
from engine.state import GameState

def get_save_path(slot: str) -> str:
    safe_slot = "".join([c for c in slot if c.isalnum() or c in ('-', '_')])
    return os.path.join(SAVE_DIR, f"{safe_slot}.json")

def save_game(state: GameState, slot: str = "slot1") -> bool:
    path = get_save_path(slot)
    data = {
        "save_version": SAVE_VERSION,
        "state": state.to_dict()
    }
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(slot: str = "slot1") -> GameState:
    path = get_save_path(slot)
    if not os.path.exists(path):
        return None
        
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        
        state = GameState()
        state.from_dict(data.get("state", {}))
        return state
    except Exception as e:
        print(f"Error loading game: {e}")
        return None

def delete_save(slot: str = "slot1") -> bool:
    path = get_save_path(slot)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
