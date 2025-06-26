import os
import json
from datetime import datetime
from pathlib import Path
from threading import Lock

class LogWriter:
    def __init__(self, base_dir="logs", debug=False):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.debug = debug
        self.lock = Lock()

    def append_entry(self, entry, label="stream"):
        """
        Append a single entry as NDJSON line to logs/stream.ndjson
        """
        filename = self.base_dir / f"{label}.ndjson"
        entry["logged_at"] = datetime.utcnow().isoformat()
        line = json.dumps(entry, ensure_ascii=False)

        try:
            with self.lock:
                with open(filename, "a", encoding="utf-8") as f:
                    f.write(line + "\n")
        except OSError as e:
            if self.debug:
                print(f"[LogWriter] failed to write to {filename}: {e}")
        return str(filename)

    def export_json(self, data, label):
        """
        Export full data as a JSON file to logs/{label}_{timestamp}.json
        """
        timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = self.base_dir / f"{label}_{timestamp}.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            if self.debug:
                print(f"[LogWriter] failed to export {filename}: {e}")
        return str(filename)
