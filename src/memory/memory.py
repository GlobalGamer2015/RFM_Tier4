import json
import os
import tempfile
from abc import ABC, abstractmethod

class MemoryManager(ABC):
    @abstractmethod
    def store_entry(self, entry: dict):
        pass

    @abstractmethod
    def fetch_recent(self, n: int) -> list:
        pass

    @abstractmethod
    def query_by_embedding(self, vec: list, top_k: int) -> list:
        pass

class GraphMemory(MemoryManager):
    def __init__(self, path="data/conversation_log.json"):
        self.path = path
        self.log = self._load_log()

    def _load_log(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def store_entry(self, entry: dict):
        self.log.append(entry)
        dirpath = os.path.dirname(self.path)
        os.makedirs(dirpath, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=dirpath)
        with os.fdopen(fd, 'w') as f:
            json.dump(self.log, f, indent=2)
        os.replace(tmp, self.path)

    def fetch_recent(self, n: int) -> list:
        return self.log[-n:]

    def query_by_embedding(self, vec: list, top_k: int) -> list:
        # Placeholder for future similarity search
        return []