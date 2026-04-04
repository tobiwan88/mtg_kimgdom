"""Game logic for MTG Advanced Kingdoms.

Each role type has a pool of named characters with unique Announce
abilities.  The official setup card defines how many characters of each
type are used per player count (5–9 players).

Role types and their card-frame colours
---------------------------------------
King     – gold / white frame
Knight   – silver / white frame
Assassin – black frame
Renegade – blue frame
Bandit   – red frame
"""

import random

# ---------------------------------------------------------------------------
# Visual style per role type (colours, icon, public flag)
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
# Named characters
#
# Keys
# ----
# role     – one of the five role types above
# life     – starting life total override (None = standard 40)
# victory  – victory condition text
# defeat   – defeat condition text (None = role-type default)
# announce – one-time Announce ability text (None = no Announce)
# passive  – always-on ability text (None = none)
# ---------------------------------------------------------------------------

CHARACTERS: dict[str, dict] = {

    # ── King ─────────────────────────────────────────────────────────────────

    "The King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            "Whenever you eliminate a player, if that player had a Knight role"
            " card, discard your hand, sacrifice half your permanents (rounded"
            " up), and lose half your life (rounded up). If you would win the"
            " game this turn, you lose the game instead."
        ),
    },

    # ── Knights ──────────────────────────────────────────────────────────────

    "The Field Marshal": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Remove all attacking creatures from combat and untap them. After"
            " this phase there is an additional combat phase. All creatures"
            " gain double strike and attack that combat if able. They can't"
            " attack you or the King that combat."
            " | Activate only during the declare blockers step on an"
            " opponent's turn."
        ),
        "passive": None,
    },
    "The Kingslayer": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated by another player.",
        "announce": (
            "Triggered when you eliminate the King — The King chooses another"
            " player. The chosen player gains the King role card. You gain a"
            " replacement Defeat condition: The King is eliminated."
        ),
        "passive": None,
    },
    "The Knight in Shining Armor": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Whenever the King would be dealt damage by an opponent this turn,"
            " deal that much damage to that opponent instead. That opponent"
            " skips their next combat step."
            " | Activate only during combat after blockers are declared."
        ),
        "passive": None,
    },
    "The Queen": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Triggered when damage dealt by another player would eliminate the"
            " King — The next time a player of your choice would deal damage to"
            " the King this turn, prevent that damage. The King gains life"
            " equal to the damage prevented this way."
        ),
        "passive": None,
    },
    "The Rightful Heir": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": (
            "The King is eliminated and the Rightful Heir is face down."
        ),
        "announce": (
            "Triggered when you eliminate a player — reveal your role."
            " When the King is eliminated, if the Rightful Heir is face up,"
            " you gain the King role card and gain 10 life."
        ),
        "passive": None,
    },

    # ── Assassins ────────────────────────────────────────────────────────────

    "The Bear Trainer": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Create three 2/2 green Bear creature tokens named War Bear. They"
            " gain haste and have 'T: This creature deals damage equal to its"
            " power to target creature. If a creature dealt damage this way"
            " dies this turn, put a +1/+1 counter on this creature.'"
            " | Activate only if an opponent has 30 or less life."
        ),
        "passive": None,
    },
    "The Marksman": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Creatures lose hexproof and shroud until end of turn. Deal"
            " damage to up to three targets equal to the highest converted"
            " mana cost among permanents you control."
        ),
        "passive": None,
    },
    "The Priestess": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Exchange life totals, accumulated commander damage, and poison"
            " counters with target player."
            " | Activate only during your turn."
        ),
        "passive": None,
    },
    "The Schemer": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Choose one — During the King's next turn, you control that player"
            " during all combat phases; or during the King's next turn, you"
            " control that player during all main phases."
            " | Activate only during your turn."
        ),
        "passive": None,
    },
    "The Thief": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Untap target permanent and gain control of it until end of turn."
            " It gains haste until end of turn."
        ),
        "passive": None,
    },

    # ── Renegades ────────────────────────────────────────────────────────────

    "The Champion": {
        "role": "Renegade",
        "life": None,
        "victory": "The Challenger is eliminated.",
        "defeat": None,
        "announce": (
            "Triggered when any player has 25 or less life — Choose a non-King"
            " opponent with the highest life total at random to become the"
            " Challenger."
        ),
        "passive": "At the beginning of your upkeep, Scry 1.",
    },
    "The Cultist": {
        "role": "Renegade",
        "life": None,
        "victory": "More than half of the players in the game are Cultists.",
        "defeat": None,
        "announce": (
            "Triggered when you would eliminate an opponent — instead, that"
            " player's role card becomes a copy of the Cultist (except it"
            " still has the King role if they were the King). Remove all"
            " commander damage and poison counters from that player. Their"
            " life total becomes 10."
        ),
        "passive": None,
    },
    "The Mimic": {
        "role": "Renegade",
        "life": None,
        "victory": "All other players are eliminated.",
        "defeat": None,
        "announce": (
            "Triggered when you have 20 or less life — draw a card."
        ),
        "passive": (
            "At the beginning of your upkeep, target player loses 1 life;"
            " another target player gains 1 life. Whenever you and any"
            " opponent have the same life total, that opponent is eliminated."
        ),
    },
    "The Sellsword": {
        "role": "Renegade",
        "life": None,
        "victory": "Your teammate wins.",
        "defeat": "You or your teammate are eliminated.",
        "announce": (
            "Triggered when any player Announces — starting with the player"
            " who triggered this ability, each player bids any amount of life"
            " in turn order. The bidding ends when the high bid stands. The"
            " high bidder loses life equal to the high bid and sacrifices a"
            " quarter of their lands (rounded up). That player becomes your"
            " teammate."
        ),
        "passive": None,
    },
    "The Straw Man": {
        "role": "Renegade",
        "life": None,
        "victory": (
            "You are the first person to be eliminated and another player"
            " eliminated you."
        ),
        "defeat": None,
        "announce": (
            "Until your next turn, all opponents' creatures must attack you if"
            " able. At the beginning of your next upkeep, you gain a"
            " replacement Victory condition: You eliminate yourself (loss of"
            " life, empty library, commander damage, or poison counters)."
            " | Activate only on your turn."
        ),
        "passive": None,
    },

    # ── Bandits ──────────────────────────────────────────────────────────────

    "The Giant": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Choose one creature with the highest combined power and"
            " toughness. Destroy the rest."
            " | Activate only during your turn."
        ),
        "passive": None,
    },
    "The Necromancer": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Exile all creature cards from target player's graveyard. An"
            " opponent with a face up role card separates those cards into two"
            " piles. Put all cards from the pile of your choice onto the"
            " battlefield under your control and exile the rest."
        ),
        "passive": None,
    },
    "The Stalker": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": "Exile target permanent.",
        "passive": None,
    },
    "The Wizard": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Choose one — Exile target spell; or change the target of target"
            " spell or ability. (Role abilities cannot be targeted.)"
        ),
        "passive": None,
    },
    "The Zealot": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Each player with a face up role card reveals cards from the top"
            " of their library until they reveal a creature card. For each"
            " creature card revealed this way you may put that card onto the"
            " battlefield under your control. Shuffle all remaining revealed"
            " cards into their owners' libraries. Those creatures gain"
            " vigilance, haste, and double strike until end of turn."
        ),
        "passive": None,
    },
}

# ---------------------------------------------------------------------------
# Official player distributions (Advanced Kingdoms setup card)
#
# 5p  — 1 King, 1 Knight, 2 Assassins, 1 Renegade
# 6p  — 1 King, 1 Knight, 2 Bandits,   2 Assassins
# 7p  — 1 King, 1 Knight, 2 Bandits,   2 Assassins, 1 Renegade
# 8p  — 1 King, 1 Knight, 2 Bandits,   3 Assassins, 1 Renegade
# 9p  — 1 King, 2 Knights, 3 Bandits,  3 Assassins
# ---------------------------------------------------------------------------

_DISTRIBUTIONS: dict[int, dict[str, int]] = {
    5: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 0, "Renegade": 1},
    6: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 2, "Renegade": 0},
    7: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 2, "Renegade": 1},
    8: {"King": 1, "Knight": 1, "Assassin": 3, "Bandit": 2, "Renegade": 1},
    9: {"King": 1, "Knight": 2, "Assassin": 3, "Bandit": 3, "Renegade": 0},
}

MIN_PLAYERS = min(_DISTRIBUTIONS)
MAX_PLAYERS = max(_DISTRIBUTIONS)


def _characters_by_role(role: str) -> list[str]:
    """Return all character names whose role type matches *role*."""
    return [
        name for name, data in CHARACTERS.items() if data["role"] == role
    ]


def make_distribution(n: int) -> list[str]:
    """Return a shuffled list of character names for *n* players.

    Randomly selects named characters within each role type according to
    the official Advanced Kingdoms setup card.

    Args:
        n: Total number of players (5–9).

    Returns:
        A shuffled list of character name strings, length == n.

    Raises:
        ValueError: If *n* is outside the supported range.
    """
    if n not in _DISTRIBUTIONS:
        raise ValueError(
            f"Advanced Kingdoms supports {MIN_PLAYERS}–{MAX_PLAYERS} players,"
            f" got {n}."
        )

    selected: list[str] = []
    for role_type, count in _DISTRIBUTIONS[n].items():
        if count == 0:
            continue
        pool = _characters_by_role(role_type)
        selected.extend(random.sample(pool, count))

    random.shuffle(selected)
    return selected
