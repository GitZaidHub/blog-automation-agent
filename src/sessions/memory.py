import time
from typing import Any, Dict, List, Optional

class Memory:
    """
    Abstractions for agent memory and session state management.
    Wraps the raw SessionService to provide structured access to context.
    """
    def __init__(self, session_service, sid: str):
        self.sessions = session_service
        self.sid = sid

    def put(self, key: str, value: Any):
        """Save a value to the session state."""
        self.sessions.update(self.sid, {key: value})

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a value from the session state."""
        data = self.sessions.get_session(self.sid)
        return data.get(key, default)

    def append_log(self, message: str, source: str = "system"):
        """
        Append a log entry to the session's history.
        Useful for tracking the agent's thought process or workflow steps.
        """
        entry = {
            "timestamp": time.time(),
            "source": source,
            "message": message
        }
        # We need to get the current logs, append, and save back.
        # Ideally, the underlying storage would support atomic appends, 
        # but for this SQLite implementation, read-modify-write is acceptable.
        current_logs = self.get("logs", [])
        if not isinstance(current_logs, list):
            current_logs = []
        current_logs.append(entry)
        self.put("logs", current_logs)

    def get_history(self) -> List[Dict]:
        """Return the full log history."""
        return self.get("logs", [])
