"""Tests for game.py — distribution and role-assignment logic."""

from collections import Counter

import pytest

from mtg_kimgdom.game import make_distribution
from mtg_kimgdom.variants import VARIANTS

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _role_counts(characters: dict, names: list[str]) -> Counter:
    """Map role → count for the given character names."""
    return Counter(characters[name]["role"] for name in names)


# ---------------------------------------------------------------------------
# make_distribution — role counts match the variant setup card
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "variant_id,n",
    [(variant_id, n) for variant_id, variant in VARIANTS.items() for n in variant["distributions"]],
)
def test_role_counts_match_distribution(variant_id: str, n: int) -> None:
    """Roles assigned to each player must exactly match the variant setup card."""
    variant = VARIANTS[variant_id]
    expected = variant["distributions"][n]
    characters = variant["characters"]

    result = make_distribution(n, variant_id)

    assert len(result) == n
    actual = _role_counts(characters, result)

    for role, count in expected.items():
        assert actual[role] == count, (
            f"{variant_id}, {n} players: expected {count}× {role}, got {actual[role]}"
        )


# ---------------------------------------------------------------------------
# make_distribution — error handling
# ---------------------------------------------------------------------------


def test_invalid_variant_raises() -> None:
    with pytest.raises(ValueError, match="Unknown variant"):
        make_distribution(5, "nonexistent_variant")


@pytest.mark.parametrize(
    "variant_id,n",
    [
        ("advanced_kingdoms_156", 2),  # below minimum
        ("advanced_kingdoms_156", 13),  # above maximum
        ("advanced_kingdoms_200", 4),  # below minimum for v2.0
        ("advanced_kingdoms_200", 10),  # above maximum for v2.0
    ],
)
def test_out_of_range_player_count_raises(variant_id: str, n: int) -> None:
    with pytest.raises(ValueError):
        make_distribution(n, variant_id)


# ---------------------------------------------------------------------------
# make_distribution — output properties
# ---------------------------------------------------------------------------


def test_output_is_shuffled_across_runs() -> None:
    """Calling make_distribution twice rarely produces the same order."""
    results = {tuple(make_distribution(12, "advanced_kingdoms_156")) for _ in range(20)}
    # With 12 players there are billions of permutations; getting the same order
    # 20 times in a row is astronomically unlikely.
    assert len(results) > 1


def test_output_contains_known_character_names() -> None:
    """Every name in the result must be a known character for that variant."""
    variant_id = "advanced_kingdoms_156"
    known = set(VARIANTS[variant_id]["characters"])
    for n in VARIANTS[variant_id]["distributions"]:
        result = make_distribution(n, variant_id)
        assert set(result).issubset(known), f"Unknown character name in result for {n} players"
