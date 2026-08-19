class Event:
    """Base class for Horror/Story events."""
    def __init__(self, event_id: str):
        self.id = event_id

    def check_trigger(self, game, action: str, target: str) -> bool:
        """Override to define when this event triggers."""
        return False

    def execute(self, game):
        """Override to define the horror effect (mutations, messages, etc)."""
        pass

class EventManager:
    def __init__(self):
        self.registered_events = []

    def register(self, event: Event):
        self.registered_events.append(event)

    def evaluate(self, game, action: str, target: str):
        """Checks all events and executes triggered ones."""
        for event in self.registered_events:
            if event.id not in game.state.session_events_triggered:
                if event.check_trigger(game, action, target):
                    event.execute(game)
                    game.state.session_events_triggered.append(event.id)
