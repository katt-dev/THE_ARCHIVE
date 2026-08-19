from engine.filesystem import VirtualFileSystem
import time

class GameState:
    def __init__(self):
        self.flags = {}
        self.inventory = []
        self.current_dir = "/"
        self.fs = VirtualFileSystem()
        self.play_time = 0
        self.session_events_triggered = []
        
        self.stats = {
            "commands_entered": 0,
            "failed_passwords": 0,
            "repeated_commands": 0,
            "last_command": "",
            "time_started": time.time(),
            "reset_count": 0,
            "meta_message": ""
        }

    def to_dict(self) -> dict:
        self.play_time += (time.time() - self.stats["time_started"])
        self.stats["time_started"] = time.time()
        
        meta = "I SEE YOU READING THIS" if self.stats["commands_entered"] > 20 else ""
        
        return {
            "flags": self.flags,
            "inventory": self.inventory,
            "current_dir": self.current_dir,
            "filesystem": self.fs.nodes,
            "play_time": self.play_time,
            "events": self.session_events_triggered,
            "stats": self.stats,
            "_WARNING_": meta
        }

    def from_dict(self, data: dict):
        self.flags = data.get("flags", {})
        self.inventory = data.get("inventory", [])
        self.current_dir = data.get("current_dir", "/")
        self.fs.nodes = data.get("filesystem", self.fs.nodes)
        self.play_time = data.get("play_time", 0)
        self.session_events_triggered = data.get("events", [])
        
        saved_stats = data.get("stats", {})
        self.stats.update(saved_stats)
        self.stats["time_started"] = time.time()
