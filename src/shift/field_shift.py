# field_shift.py

from typing import Dict, List, Any


class FieldShift:
    @staticmethod
    def detect(
        tone_vector: Dict[str, Any],
        persona_profile: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """
        Detects significant emotional field shifts by comparing
        a tone vector against persona-specific thresholds.

        Args:
            tone_vector: {
                "dominant_tone": "CALM",
                "vector": {"CALM": 0.6, "ANGER": 0.2, ...}
            }
            persona_profile: {
                "CALM": 0.5,
                "ANGER": 0.4,
                ...
            }

        Returns:
            A list of shift event dicts, each with:
            - emotion: the dimension name
            - value: the observed score
            - threshold: persona threshold
            - delta: abs(value - threshold)
            - severity: "mild" | "moderate" | "extreme"
            - type: "field_shift"
            - dominant_tone: optional context
        """
        shifts: List[Dict[str, Any]] = []
        vector = tone_vector.get("vector", {})
        dominant = tone_vector.get("dominant_tone")

        for emotion, raw in vector.items():
            # Skip non-numeric entries
            if not isinstance(raw, (int, float)):
                continue

            threshold = persona_profile.get(emotion, 0.5)
            delta = abs(raw - threshold)

            # detect significant shifts
            if delta <= 0.3:
                continue

            shifts.append({
                "emotion": emotion,
                "value": raw,
                "threshold": threshold,
                "delta": round(delta, 3),
                "severity": FieldShift._classify_severity(delta),
                "type": "field_shift",
                **({"dominant_tone": dominant} if dominant else {})
            })

        return shifts

    @staticmethod
    def _classify_severity(delta: float) -> str:
        """
        Maps numeric delta to a symbolic severity label.
        """
        if delta > 0.6:
            return "extreme"
        if delta > 0.4:
            return "moderate"
        return "mild"
