# recursive_replayer.py

from memory.graph_memory import GraphMemory
from engine.tone import ToneLabel

class RecursiveReplayer:
    def __init__(self, memory: GraphMemory):
        self.memory = memory

    def replay(self, n=5):
        summaries = self.memory.fetch_recent(n)
        full = [self.memory.fetch_expanded(summary) for summary in summaries]
        return full
