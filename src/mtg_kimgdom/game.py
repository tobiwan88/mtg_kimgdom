"""Game logic for MTG Commander Kingdom.

Public API
----------
ROLE_STYLES      – visual style data per role type (colour, icon, public flag)
VARIANTS         – registry of all available variants (re-exported from variants/)
DEFAULT_VARIANT  – id of the default variant (re-exported from variants/)
MIN_PLAYERS      – minimum player count supported by the default variant
MAX_PLAYERS      – maximum player count supported by the default variant
make_distribution(n, variant_id) – return a shuffled character assignment for n players
"""

import random

from mtg_kimgdom.variants import DEFAULT_VARIANT, VARIANTS

__all__ = [
    "DEFAULT_VARIANT",
    "MAX_PLAYERS",
    "MIN_PLAYERS",
    "ROLE_STYLES",
    "VARIANTS",
    "make_distribution",
]

# ---------------------------------------------------------------------------
# Visual style per role type (colours, icon, public flag)
# Shared across all variants — extend here if a new variant adds role types.
# ---------------------------------------------------------------------------

ROLE_STYLES: dict[str, dict] = {
    "King": {
        "color": "#FFD700",
        "border": "#b8860b",
        "icon": "👑",
        "public": True,
        "team": "Royal",
    },
    "Knight": {
        "color": "#e0e0e0",
        "border": "#78909c",
        "icon": "⚔️",
        "public": False,
        "team": "Royal",
    },
    "Assassin": {
        "color": "#cfd8dc",
        "border": "#263238",
        "icon": "🗡️",
        "public": False,
        "team": "Assassins",
    },
    "Renegade": {
        "color": "#90caf9",
        "border": "#1565c0",
        "icon": "🌀",
        "public": False,
        "team": "None",
    },
    "Bandit": {
        "color": "#ef9a9a",
        "border": "#b71c1c",
        "icon": "💀",
        "public": False,
        "team": "Bandits",
    },
}

# ---------------------------------------------------------------------------
# Backwards-compatible constants derived from the default variant
# ---------------------------------------------------------------------------

_default_distributions = VARIANTS[DEFAULT_VARIANT]["distributions"]
MIN_PLAYERS = min(_default_distributions)
MAX_PLAYERS = max(_default_distributions)


# ---------------------------------------------------------------------------
# Distribution helpers
# ---------------------------------------------------------------------------


def _characters_by_role(role: str, characters: dict[str, dict]) -> list[str]:
    """Return all character names whose role type matches *role*."""
    return [name for name, data in characters.items() if data["role"] == role]


def make_distribution(n: int, variant_id: str = DEFAULT_VARIANT) -> list[str]:
    """Return a shuffled list of character names for *n* players.

    Randomly selects named characters within each role type according to
    the setup card of the chosen variant.

    Args:
        n:          Total number of players.
        variant_id: Key into VARIANTS (defaults to DEFAULT_VARIANT).

    Returns:
        A shuffled list of character name strings, length == n.

    Raises:
        ValueError: If *variant_id* is unknown or *n* is out of range.
    """
    if variant_id not in VARIANTS:
        raise ValueError(f"Unknown variant: {variant_id!r}.")

    variant = VARIANTS[variant_id]
    distributions = variant["distributions"]
    characters = variant["characters"]
    min_p, max_p = min(distributions), max(distributions)

    if n not in distributions:
        raise ValueError(f"{variant['name']} supports {min_p}–{max_p} players, got {n}.")

    selected: list[str] = []
    for role_type, count in distributions[n].items():
        if count == 0:
            continue
        pool = _characters_by_role(role_type, characters)
        selected.extend(random.sample(pool, count))

    random.shuffle(selected)
    return selected
