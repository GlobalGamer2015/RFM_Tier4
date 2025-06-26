
from enum import Enum, auto
from typing import Dict, Any

class TokenQual(Enum):
    QUALIFIED = auto()
    AMBIGUOUS = auto()
    UNSTABLE = auto()

class TokenQualifier:
    def __init__(self,
                 symbolic_threshold: int = 2,
                 volatility_threshold: float = 0.5) -> None:
        """
        :param symbolic_threshold: minimum number of symbolic tags
        :param volatility_threshold: minimum field_intensity to count as unstable
        """
        self.symbolic_threshold = symbolic_threshold
        self.volatility_threshold = volatility_threshold

    def qualify(self, node: Dict[str, Any]) -> TokenQual:
        """
        Classify a token node into QUALIFIED, AMBIGUOUS or UNSTABLE.
        """
        vec = node.get("symbolic_vector", [])
        intensity = node.get("field_intensity", 0.0)

        if len(vec) >= self.symbolic_threshold and intensity >= self.volatility_threshold:
            return TokenQual.UNSTABLE
        elif len(vec) >= self.symbolic_threshold:
            return TokenQual.AMBIGUOUS
        else:
            return TokenQual.QUALIFIED
