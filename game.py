"""Game logic for MTG Commander Kingdom.

Defines the five roles, their win conditions, and the function that
produces a shuffled role list for a given player count.
"""

import random

# ---------------------------------------------------------------------------
# Role definitions
# ---------------------------------------------------------------------------

ROLES: dict[str, dict] = {
    "King": {
        "color": "#FFD700",
        "border": "#b8860b",
        "icon": "👑",
        "team": "Royal",
        "public": True,
        "life": 50,
        "description": (
            "Your identity is revealed to all players at the start of the"
            " game. You begin with <strong>50 life</strong> instead of 40."
        ),
        "win": "Win if only you and your Knights remain alive.",
    },
    "Knight": {
        "color": "#4FC3F7",
        "border": "#0288d1",
        "icon": "⚔️",
        "team": "Royal",
        "public": False,
        "life": None,
        "description": "You serve the King. Keep your role hidden.",
        "win": (
            "Win alongside the King if all Assassins, Bandits, and"
            " Renegades are eliminated."
        ),
    },
    "Assassin": {
        "color": "#EF5350",
        "border": "#b71c1c",
        "icon": "🗡️",
        "team": "Assassins",
        "public": False,
        "life": None,
        "description": "You seek the King's head. Keep your role hidden.",
        "win": (
            "Win by being the last player standing. "
            "You must outlive all Bandits — if a Bandit is alive when"
            " the King dies, the Bandits win instead."
        ),
    },
    "Bandit": {
        "color": "#AB47BC",
        "border": "#6a1b9a",
        "icon": "💀",
        "team": "Bandits",
        "public": False,
        "life": None,
        "description": "You scheme against the King. Keep your role hidden.",
        "win": (
            "Win if at least one Bandit is still alive when the King"
            " is eliminated."
        ),
    },
    "Renegade": {
        "color": "#66BB6A",
        "border": "#2e7d32",
        "icon": "🌀",
        "team": "None",
        "public": False,
        "life": None,
        "description": "You walk alone. Keep your role hidden.",
        "win": "Win by being the very last player standing.",
    },
}

# ---------------------------------------------------------------------------
# Role distributions
# ---------------------------------------------------------------------------

_DISTRIBUTIONS: dict[int, list[str]] = {
    3: ["King", "Assassin", "Bandit"],
    4: ["King", "Knight", "Assassin", "Bandit"],
    5: ["King", "Knight", "Assassin", "Bandit", "Renegade"],
    6: ["King", "Knight", "Knight", "Assassin", "Bandit", "Renegade"],
    7: [
        "King", "Knight", "Knight",
        "Assassin", "Assassin", "Bandit", "Renegade",
    ],
    8: [
        "King", "Knight", "Knight",
        "Assassin", "Assassin", "Bandit", "Bandit", "Renegade",
    ],
    9: [
        "King", "Knight", "Knight", "Knight",
        "Assassin", "Assassin", "Bandit", "Bandit", "Renegade",
    ],
    10: [
        "King", "Knight", "Knight", "Knight",
        "Assassin", "Assassin", "Bandit", "Bandit",
        "Renegade", "Renegade",
    ],
}

_MIN_PLAYERS = 3
_MAX_PLAYERS = 12


def make_distribution(n: int) -> list[str]:
    """Return a shuffled list of role names for *n* players.

    Args:
        n: Total number of players (3–12).  Values outside the preset
           table are handled by scaling up from the 10-player base.

    Returns:
        A new shuffled list of role name strings.
    """
    if n in _DISTRIBUTIONS:
        roles = _DISTRIBUTIONS[n][:]
    elif n > max(_DISTRIBUTIONS):
        base = _DISTRIBUTIONS[max(_DISTRIBUTIONS)][:]
        for i in range(n - max(_DISTRIBUTIONS)):
            base.append("Knight" if i % 2 == 0 else "Assassin")
        roles = base
    else:
        roles = _DISTRIBUTIONS[_MIN_PLAYERS][:]

    random.shuffle(roles)
    return roles
