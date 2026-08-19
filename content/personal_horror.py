import getpass
import urllib.request
import json
from engine.terminal import slow_print

def get_location():
    """Fetches the player's city based on their public IP using a free API."""
    try:
        with urllib.request.urlopen("http://ip-api.com/json/", timeout=3) as response:
            data = json.loads(response.read().decode())
            return data.get("city", "your town")
    except Exception:
        return "your town"

def run_pre_game_setup(game):
    print("========================================")
    print("        SYSTEM CALIBRATION              ")
    print("========================================\n")
    
    print("For the intended psychological horror experience, this game can use real-world data.")
    print("Data is processed ONLY on your local machine and never saved externally.\n")
    
    pc_consent = input("Do you allow the game to use your PC username? (y/n): ").strip().lower()
    ip_consent = input("Do you allow the game to ping your public IP to find your general area? (y/n): ").strip().lower()
    
    print("\nProcessing...")
    if pc_consent == 'y':
        game.state.flags["pc_name"] = getpass.getuser()
    if ip_consent == 'y':
        game.state.flags["real_location"] = get_location()

    print("\n========================================")
    print("             HOW TO PLAY                ")
    print("========================================\n")
    print("1. You are interacting with a simulated command-line interface.")
    print("2. Type 'help' to see a list of valid commands.")
    print("3. Use 'ls' to list files, 'cd <folder>' to change directories, and 'cat <file>' to read.")
    print("4. Your goal is to uncover what happened to the original researchers.")
    print("5. Start your investigation by reading the README.txt file.")
    print("\n========================================\n")
    
    input("Press ENTER to initialize THE ARCHIVE...")
