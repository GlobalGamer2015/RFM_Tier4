# run.py — Tier 4 RFM Companion AI Runner

import time
import uuid
from analyzer.token_qualifier import TokenQualifier
from engine.tone import ToneEngine
from shift.field_shift import FieldShift
from memory.memory import GraphMemory
from persona.persona import Persona
from logger.logger import SessionLogger
from playback.replayer import RecursiveReplayer  # ✅ Correct class

def tokenize(text):
    # Simple whitespace tokenizer; replace with NLP-aware tokenizer as needed
    return text.strip().split()

def main():
    print("🤖 RFM Tier 4-G Companion AI — Type something to begin (or 'exit' to quit).")

    # Instantiate core components
    qualifier     = TokenQualifier()
    tone_engine   = ToneEngine()
    memory        = GraphMemory()
    persona       = Persona(name="Jordan")
    logger        = SessionLogger()
    replayer      = RecursiveReplayer(memory)  # ✅ FIXED: pass memory to constructor

    while True:
        text = input("You: ")
        if text.strip().lower() in {"exit", "quit"}:
            print("Goodbye.")
            break
        if not text.strip():
            continue

        # Tokenize and annotate
        tokens = tokenize(text)
        token_nodes = []
        for tok in tokens:
            node = {"token": tok, "field_intensity": 0.0}
            qual = qualifier.qualify(node)
            node["qualification"] = qual.name  # or str(qual)
            token_nodes.append(node)

        # Tone and field inference
        tone_vector = tone_engine.infer(token_nodes)
        shift_events = FieldShift.detect(tone_vector, persona.profile)

        # Memory update
        memory.store_entry({
            "id": uuid.uuid4().hex,
            "timestamp": time.time(),
            "tone": tone_vector.get("dominant_tone", "FLAT"),
            "token_data": token_nodes
        })

        # Persona reaction
        response = persona.react(tone_vector, shift_events)
        persona.last_reply = response
        print(f"Jordan: {response}")

        # Logging
        logger.write({
            "input": text,
            "tokens": token_nodes,
            "tone": tone_vector,
            "shifts": shift_events,
            "response": response
        })

if __name__ == "__main__":
    main()
