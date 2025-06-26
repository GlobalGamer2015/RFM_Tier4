# graph_memory.py

import uuid
import time
from collections import defaultdict
from abc import ABC, abstractmethod
from memory.memory import MemoryManager
from engine.tone import ToneLabel

# ──────────────────────────────────────────────────────────────────────────────
# 1. Symbolic Inferencer Strategy (pluggable)
# ──────────────────────────────────────────────────────────────────────────────
class SymbolicInferencer(ABC):
    @abstractmethod
    def infer_vector(self, token: str) -> list:
        pass

    @abstractmethod
    def infer_link_groups(self, symbolic_vector: list) -> list:
        pass

class DefaultSymbolicInferencer(SymbolicInferencer):
    def infer_vector(self, token: str) -> list:
        looney_refs = {
            "daffy": "Daffy Duck",
            "bugs":  "Bugs Bunny",
            "elmer": "Elmer Fudd",
            "loony": "Looney Tunes"
        }
        return [v for k, v in looney_refs.items() if k in token.lower()]

    def infer_link_groups(self, symbolic_vector: list) -> list:
        groups = []
        if any("Looney Tunes" in s for s in symbolic_vector):
            groups.append("looney_tunes_001")
        return groups


# ──────────────────────────────────────────────────────────────────────────────
# 2. TokenNode with bidirectional links & metadata
# ──────────────────────────────────────────────────────────────────────────────
class TokenNode:
    def __init__(
        self,
        text: str,
        tone: ToneLabel,
        field_intensity: float,
        recursion_parent: str = None,
        symbolic_vector: list = None,
        link_groups: list = None
    ):
        self.id = str(uuid.uuid4())
        self.text = text
        self.tone = tone
        self.field_intensity = field_intensity
        self.recursion_parent = recursion_parent
        self.recursion_children = []
        self.symbolic_vector = symbolic_vector or []
        self.link_groups = link_groups or []
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "tone": self.tone.name,
            "field_intensity": self.field_intensity,
            "recursion_parent": self.recursion_parent,
            "recursion_children": self.recursion_children,
            "symbolic_vector": self.symbolic_vector,
            "link_groups": self.link_groups,
            "timestamp": self.timestamp
        }


# ──────────────────────────────────────────────────────────────────────────────
# 3. GraphMemory Implementation
# ──────────────────────────────────────────────────────────────────────────────
class GraphMemory(MemoryManager):
    def __init__(self, inferencer: SymbolicInferencer = None):
        self.nodes = {}                    # id → TokenNode
        self.entries = []                  # utterance-level summaries
        self.link_groups = defaultdict(list)
        self.inferencer = inferencer or DefaultSymbolicInferencer()

    def store_entry(self, entry: dict):
        """
        Stores a new utterance entry in the graph.

        entry: {
            'id': str,
            'timestamp': float (optional),
            'tone': ToneLabel or tone string,
            'token_data': [
                {'token': str, 'field_intensity': float}, ...
            ]
        }
        """
        ts = entry.get("timestamp", time.time())
        tone = entry.get("tone")
        if isinstance(tone, str):
            tone = ToneLabel[tone]

        root_ids = []
        prev_id = None

        for tok in entry["token_data"]:
            text = tok["token"]
            intensity = tok.get("field_intensity", 0.0)
            vec = self.inferencer.infer_vector(text)
            groups = self.inferencer.infer_link_groups(vec)

            node = TokenNode(
                text=text,
                tone=tone,
                field_intensity=intensity,
                recursion_parent=prev_id,
                symbolic_vector=vec,
                link_groups=groups
            )

            if prev_id:
                self.nodes[prev_id].recursion_children.append(node.id)

            self.nodes[node.id] = node
            tok["id"] = node.id
            root_ids.append(node.id)

            for g in groups:
                self.link_groups[g].append(node.id)

            prev_id = node.id

        prev_utt_id = self.entries[-1]["utterance_id"] if self.entries else None
        self.entries.append({
            "utterance_id": entry["id"],
            "timestamp": ts,
            "dominant_tone": tone.name,
            "token_ids": root_ids,
            "prev_utterance_id": prev_utt_id
        })

    def fetch_recent(self, n: int) -> list:
        return self.entries[-n:]

    def fetch_expanded(self, utterance_summary: dict) -> list:
        return [self.nodes[nid].to_dict() for nid in utterance_summary["token_ids"]]

    def query_by_embedding(self, vec: list, top_k: int) -> list:
        return []  # reserved for future vector-based lookup
