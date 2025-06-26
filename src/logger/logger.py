# src/logger/logger.py

from audit.logwriter import LogWriter

# Compatibility alias for run.py
class SessionLogger(LogWriter):
    def write(self, entry):
        # Auto-convert custom objects in 'tokens' if present
        if "tokens" in entry:
            entry["tokens"] = [
                t.to_dict() if hasattr(t, "to_dict") else
                t.__dict__ if hasattr(t, "__dict__") else
                str(t)
                for t in entry["tokens"]
            ]
        self.append_entry(entry)
