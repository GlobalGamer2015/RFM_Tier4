
from token_qualifier import TokenQualifier, TokenQual

def test_qualified():
    tq = TokenQualifier()
    node = {"symbolic_vector": [], "field_intensity": 0.2}
    assert tq.qualify(node) == TokenQual.QUALIFIED

def test_ambiguous():
    tq = TokenQualifier()
    node = {"symbolic_vector": ["a", "b", "c"], "field_intensity": 0.2}
    assert tq.qualify(node) == TokenQual.AMBIGUOUS

def test_unstable():
    tq = TokenQualifier()
    node = {"symbolic_vector": ["a", "b", "c"], "field_intensity": 0.6}
    assert tq.qualify(node) == TokenQual.UNSTABLE

def test_exact_thresholds():
    tq = TokenQualifier(symbolic_threshold=2, volatility_threshold=0.5)
    node = {"symbolic_vector": ["A","B"], "field_intensity": 0.5}
    assert tq.qualify(node) == TokenQual.UNSTABLE

def test_defaults_missing():
    tq = TokenQualifier()
    assert tq.qualify({}) == TokenQual.QUALIFIED
