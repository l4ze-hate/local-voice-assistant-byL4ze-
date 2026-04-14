"""Command history manager with search functionality."""
from datetime import datetime


class CommandHistory:
    """Stores and manages command history."""

    def __init__(self, max_entries=100):
        self.max_entries = max_entries
        self.history = []

    def add_entry(self, command, response, entry_type="command"):
        """Add a new entry to history."""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "command": command,
            "response": response,
            "type": entry_type
        }
        self.history.append(entry)
        if len(self.history) > self.max_entries:
            self.history.pop(0)

    def search(self, query):
        """Search history for matching query."""
        if not query:
            return self.history
        
        query_lower = query.lower()
        return [
            entry for entry in self.history
            if query_lower in entry["command"].lower() 
            or query_lower in entry["response"].lower()
        ]

    def clear(self):
        """Clear all history."""
        self.history.clear()

    def get_all(self):
        """Get all history entries."""
        return self.history.copy()
