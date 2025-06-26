# RFM Tier 4 — Resonant Field Mapping Companion AI

**Tier 4** of the PUTMAN Model introduces a fully modular, local-friendly emotional companion AI designed to process symbolic language, infer emotional tone, and track conversational field shifts in real time.

## 🔍 Overview

This Tier 4 implementation includes:
- Token qualification and emotional tone inference
- Field shift detection (e.g., suspicion, anger, joy)
- Symbolic memory via graph nodes
- Persona response logic
- Logging and REPL loop for human-AI interaction

## 🚀 Quick Start

```bash
python run.py
```

Then type your message to the AI. Example:
```
You: I had a strange dream about light and mirrors.
Jordan: That sounds intense. Dreams often carry symbolic resonance. Want to explore it?
```

## 📂 Modules

- `qualifier.py` — Assigns symbolic/emotional tags to tokens.
- `tone_engine.py` — Infers affect vector from qualified tokens.
- `memory.py` — Stores symbolic conversational history.
- `persona.py` — Generates responses based on profile and tone.
- `fieldshift.py` — Detects emotional field changes.
- `logger.py` — Writes interaction logs.
- `replayer.py` — Optional replay of past sessions.
- `run.py` — CLI runner with integrated components.

## 🧠 Based On

PUTMAN Model & Resonant Field Mapping (RFM): A symbolic emotional architecture for empathic AI.

For Tier 5 (emotional physics, decision rationales, visual HUDs), see upcoming releases.

## 📜 License

This work is licensed under **CC BY-NC 4.0** — free for personal, research, and non-commercial use. See LICENSE for full terms.
