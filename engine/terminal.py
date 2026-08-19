import sys
import time
import random

def slow_print(text: str, speed: float = 0.03, glitch_chance: float = 0.0):
    """Prints text character by character to simulate a real terminal."""
    for char in text:
        if glitch_chance > 0 and random.random() < glitch_chance:
            sys.stdout.write(random.choice(['#', '%', '&', '?', '█', '░']))
            sys.stdout.flush()
            time.sleep(speed * 2)
            sys.stdout.write('\b' + char)
        else:
            sys.stdout.write(char)
        sys.stdout.flush()
        
        if char in ['.', '!', '?']:
            time.sleep(speed * 10)
        elif char == '\n':
            time.sleep(speed * 5)
        else:
            time.sleep(speed + (random.uniform(-0.01, 0.02)))
    print()

def simulate_crash():
    """Simulates a harmless fake terminal crash."""
    time.sleep(1)
    slow_print("\nFATAL EXCEPTION: 0x00000008 [MEMORY ACCESS VIOLATION]", 0.01)
    slow_print("Dumping physical memory to disk...", 0.05)
    for i in range(1, 101, 17):
        print(f"Dump at {i}%")
        time.sleep(0.2)
    print("Dump complete.")
    time.sleep(1)
    print("Rebooting sandboxed environment...\n")
    time.sleep(2)
