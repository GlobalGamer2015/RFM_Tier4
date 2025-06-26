# persona.py

from enum import Enum
from typing import Optional

class PersonaMode(Enum):
    UTILITY   = "utility"
    COMPANION = "companion"
    THERAPIST = "therapist"
    DEBUG     = "debug"


class PersonaConfig:
    def __init__(self, mode: PersonaMode):
        self.mode = mode
        # set defaults for every attribute so you never hit an AttributeError
        self.memory_type: str          = "flat"
        self.track_tone: bool          = False
        self.track_recursion: bool     = False
        self.detect_shifts: bool       = False
        self.field_shift_sensitivity: float = 0.4
        self.enable_debug_output: bool = False

        self.apply_mode()

    def apply_mode(self) -> None:
        if self.mode == PersonaMode.UTILITY:
            # all defaults are fine
            pass

        elif self.mode == PersonaMode.COMPANION:
            self.memory_type          = "graph"
            self.track_tone           = True
            self.track_recursion      = True
            self.detect_shifts        = True

        elif self.mode == PersonaMode.THERAPIST:
            self.memory_type          = "graph"
            self.track_tone           = True
            self.track_recursion      = True
            self.detect_shifts        = True
            self.field_shift_sensitivity = 0.25  # stricter

        elif self.mode == PersonaMode.DEBUG:
            self.memory_type          = "graph"
            self.track_tone           = True
            self.track_recursion      = True
            self.detect_shifts        = True
            self.enable_debug_output  = True

class Persona:
    def __init__(self, name="Jordan", mode=PersonaMode.COMPANION):
        self.name = name
        self.config = PersonaConfig(mode)
        self.last_reply = ""

        # mimic `profile` expected by run.py for now
        self.profile = {
            "baseline_tone": "NEUTRAL",
            "shift_sensitivity": self.config.field_shift_sensitivity
        }

    def react(self, tone_vector, shift_events):
        dominant = tone_vector.get("dominant_tone", "FLAT")
        response = ""

        if self.config.detect_shifts and shift_events:
            response += f"(Tone shift detected: {shift_events}) "

        if self.config.track_tone:
            match dominant:
                case "NEGATIVE":
                    response += "I'm sensing some negativity. Want to talk about it?"
                case "POSITIVE":
                    response += "That sounds great! I'm with you."
                case "NEUTRAL":
                    response += "I'm here, listening."
                case _:
                    response += "Hmm, I'm not sure how to respond yet."
        else:
            response += "How can I assist you today?"

        return response
