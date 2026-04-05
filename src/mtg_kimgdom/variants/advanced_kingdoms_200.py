"""Advanced Kingdoms v2.0 variant — latest ruleset (5–9 players).

Key changes from v1.56
----------------------
- Kings    : Passive simplified (eliminated if you kill a Knight). Beloved
             Kings expansion adds 5 named Kings to the King pool.
- Knights  : 'The Knight in Shining Armor' renamed to 'The Guardmage' (same
             ability). Field Commander now grants menace (was double strike).
             Rightful Heir also untaps all permanents on ascending to King.
- Assassins: The Thief controls until beginning of next end step (not EOT).
- Bandits  : The Stalker gains Split Second. The Zealot targets MV 4+.
             The Necromancer mills 10 first; stolen creatures gain indestructible.
- Renegades: The Mimic draws two cards on Announce (was one). The Cultist sets
             converted player's life to 15 (was 10). The Sellsword sacrifices a
             land each (was quarter of lands).

Character pool
--------------
Kings    : The King, The Brash King, The Cruel King, The Fair King,
           The Generous King, The Wise King
Knights  : The Field Commander, The Guardmage, The Kingslayer,
           The Queen, The Rightful Heir
Assassins: The Bear Trainer, The Marksman, The Priestess, The Schemer, The Thief
Renegades: The Champion, The Cultist, The Mimic, The Sellsword, The Straw Man
Bandits  : The Giant, The Necromancer, The Stalker, The Wizard, The Zealot
"""

VARIANT_ID = "advanced_kingdoms_200"

# ---------------------------------------------------------------------------
# Player distributions (5–9 players)
# ---------------------------------------------------------------------------

_DISTRIBUTIONS: dict[int, dict[str, int]] = {
    5: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 0, "Renegade": 1},
    6: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 2, "Renegade": 0},
    7: {"King": 1, "Knight": 1, "Assassin": 2, "Bandit": 2, "Renegade": 1},
    8: {"King": 1, "Knight": 1, "Assassin": 3, "Bandit": 2, "Renegade": 1},
    9: {"King": 1, "Knight": 1, "Assassin": 3, "Bandit": 3, "Renegade": 1},
}

# ---------------------------------------------------------------------------
# Shared tip pools (avoid repetition across characters of the same role)
# ---------------------------------------------------------------------------

_KING_BASE_PASSIVE = (
    "Keep the King face up at all times."
    " Whenever you eliminate a player, if that player had a Knight role card,"
    " you are eliminated."
)

_KING_BASE_TIPS = [
    "You are guaranteed to have a secret ally — a Knight — in your Kingdom."
    " Seek out their identity as soon as possible.",
    "Think twice before eliminating any face-down player."
    " Eliminating your Knight causes your immediate elimination.",
    "Assassins will likely pretend to be friendly early game."
    " Be wary of small gestures made to gain your favor.",
    "The King and Bandits have a temporary alliance — both want the Assassins gone."
    " But once the Assassins are eliminated, the Bandits will turn on you.",
]

_KNIGHT_BASE_TIPS = [
    "Knights are the secret protectors of the kingdom. Serve your King well.",
    "You win by keeping your King alive and ridding the kingdom of all who seek to do him harm.",
    "In the early game, Assassins and Renegades may publicly claim to be Knights."
    " As the true Knight you should target these enemies for elimination.",
    "Assassins are your primary target. Once eliminated, shift focus to Bandits and Renegades.",
]

_ASSASSIN_BASE_TIPS = [
    "Assassins have one task in mind: kill the King.",
    "There is always more than one hidden Assassin in play."
    " Pay close attention to in-game actions to identify your hidden ally.",
    "You are not truly teammates with other Assassins until both have Announced publicly.",
    "Your primary goal is to kill the King — all non-Assassin Roles will want to see you dead first.",
]

_BANDIT_BASE_TIPS = [
    "Bandits maintain balance within the kingdom."
    " If any Bandit is eliminated, all Bandits are immediately eliminated — protect your teammates.",
    "Your first priority is to identify and eliminate the Assassins."
    " If the King dies while any Assassin lives, the Assassins immediately win.",
    "After the Assassins are gone, break your truce with the King."
    " Eliminate the King and all other non-Bandits to win.",
]

# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

_CHARACTERS: dict[str, dict] = {
    # ── King (base) ───────────────────────────────────────────────────────────
    "The King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": _KING_BASE_PASSIVE,
        "tips": _KING_BASE_TIPS,
        "clarifications": [],
    },
    # ── Beloved Kings (expansion) ─────────────────────────────────────────────
    "The Brash King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            _KING_BASE_PASSIVE
            + " At the beginning of each player's upkeep, that player exiles the top card"
            " of their library. They may play it that turn."
        ),
        "tips": _KING_BASE_TIPS
        + [
            "Your upkeep ability gives all players impulse draw each turn — games will move fast.",
        ],
        "clarifications": [],
    },
    "The Cruel King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            _KING_BASE_PASSIVE
            + " At the beginning of each player's upkeep, that player loses 2 life."
        ),
        "tips": _KING_BASE_TIPS
        + [
            "Your upkeep ability drains all players of 2 life each turn — eliminations will come quickly.",
        ],
        "clarifications": [],
    },
    "The Fair King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            _KING_BASE_PASSIVE
            + " At the beginning of each player's end step, if that player controls fewer lands than"
            " target oppnent, that player may search their library for a baisc land card, put that"
            " card onto the battlefield, then shuffle"
        ),
        "tips": _KING_BASE_TIPS
        + [
            "Your upkeep ability rewards the leading player, creating political pressure to target them.",
        ],
        "clarifications": [],
    },
    "The Generous King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            _KING_BASE_PASSIVE
            + " At the beginning of each player's precombat main phase, that player adds {C}."
        ),
        "tips": _KING_BASE_TIPS
        + [
            "Your ability gives all players free mana each turn, enabling explosive plays.",
        ],
        "clarifications": [],
    },
    "The Wise King": {
        "role": "King",
        "life": 50,
        "victory": "All Assassins, Bandits and Renegades are eliminated.",
        "defeat": None,
        "announce": None,
        "passive": (
            _KING_BASE_PASSIVE + " At the beginning of each player's upkeep, that player scries 1."
        ),
        "tips": _KING_BASE_TIPS
        + [
            "Your upkeep ability gives all players a scry each turn, smoothing out draws.",
        ],
        "clarifications": [],
    },
    # ── Knights ───────────────────────────────────────────────────────────────
    "The Field Commander": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Remove all attacking creatures from combat and untap them. After this phase,"
            " there is an additional combat phase. All creatures gain menace and attack next"
            " combat if able. They can't attack you or the King that combat."
            " | Activate only during the declare blockers step on an opponent's turn."
        ),
        "passive": None,
        "tips": _KNIGHT_BASE_TIPS
        + [
            "As the Field Commander, confuse your enemies to fight amongst themselves."
            " Announce strategically and take advantage of the chaos after the battle.",
        ],
        "clarifications": [
            "Can only Announce on an opponent's turn, during combat, after blockers are declared.",
            "Even creatures that did not attack originally are required to attack in the additional"
            " combat phase. Those creatures can't attack the Field Commander or the King.",
        ],
    },
    "The Guardmage": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Whenever the King would be dealt damage by an opponent this turn,"
            " deal that much damage to that opponent instead."
            " That opponent skips their next combat step."
            " | Activate only during combat after blockers are declared."
        ),
        "passive": None,
        "tips": _KNIGHT_BASE_TIPS
        + [
            "As the Guardmage, no damage is dealt to the King — instead it is redirected to the attacker.",
            "The King likely won't anticipate your ability. If you can convince the King to leave"
            " a large amount of damage unblocked, it can work in both your favors.",
        ],
        "clarifications": [
            "Can only Announce during combat after blockers are declared.",
        ],
    },
    "The Kingslayer": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated by another player.",
        "announce": (
            "Triggered when you eliminate the King — The King chooses an opponent."
            " The chosen player gains the King role card."
            " You have a replacement Defeat condition: The King is eliminated."
        ),
        "passive": None,
        "tips": _KNIGHT_BASE_TIPS
        + [
            "As the Kingslayer, you have a backup plan if the King is unfit to rule."
            " Turning against the King is a last resort — the King's choice of successor"
            " may reflect how they viewed your loyalty.",
        ],
        "clarifications": [
            "The King cannot choose the Kingslayer to be the new King.",
            "When a new King is chosen, the chosen player gains the King role card"
            " and discards their previous role card.",
        ],
    },
    "The Queen": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated.",
        "announce": (
            "Triggered when damage dealt by another player would eliminate the King —"
            " The next time a player of your choice would deal damage to the King this turn,"
            " prevent that damage. The King gains life equal to the damage prevented this way."
        ),
        "passive": None,
        "tips": _KNIGHT_BASE_TIPS
        + [
            "As the Queen, you live to protect your King."
            " Save his life by stalling his assailants while he heals his wounds.",
        ],
        "clarifications": [
            "Can only Announce if one of the following is true: the King is being attacked by unblocked"
            " creatures with total power ≥ the King's life total; targeted by non-combat damage ≥ the"
            " King's life total; or attacked by an unblocked commander with power greater than the"
            " remaining commander-damage threshold.",
        ],
    },
    "The Rightful Heir": {
        "role": "Knight",
        "life": None,
        "victory": "The King wins.",
        "defeat": "The King is eliminated and the Rightful Heir is face down.",
        "announce": (
            "Triggered when you eliminate a player — reveal your role."
            " When the King is eliminated, if the Rightful Heir is face up,"
            " you gain the King role card."
            " If you do, gain 10 life and untap all permanents you control."
        ),
        "passive": None,
        "tips": _KNIGHT_BASE_TIPS
        + [
            "As the Rightful Heir, prove yourself worthy by eliminating one of your father's enemies."
            " After doing so, if the King falls you will take your place on the throne.",
        ],
        "clarifications": [
            "When you eliminate any player, you are required to Announce as a triggered ability.",
            "If you are eliminated before Announcing, you immediately lose.",
            "When you gain the King Role card, discard the Rightful Heir Role card.",
            "The Rightful Heir is eliminated if they eliminate the King"
            " (they are face down when the King is eliminated).",
        ],
    },
    # ── Assassins ─────────────────────────────────────────────────────────────
    "The Bear Trainer": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Create three 2/2 green Bear creature tokens named War Bear. They have"
            " 'T: This creature deals damage equal to its power to target creature."
            " If a creature dealt damage this way dies this turn,"
            " put a +1/+1 counter on this creature.'"
            " | Activate only if an opponent has 30 or less life."
        ),
        "passive": None,
        "tips": _ASSASSIN_BASE_TIPS
        + [
            "As the Bear Trainer, the War Bears can quickly eat through an enemy's battlefield."
            " Use them to clear the way for large-scale attacks.",
        ],
        "clarifications": [
            "This is an activated ability — can be used any time as long as any opponent has 30 or less life.",
        ],
    },
    "The Marksman": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Creatures lose hexproof and shroud until end of turn."
            " Deal damage to up to three targets equal to the highest converted mana cost"
            " among permanents you control."
        ),
        "passive": None,
        "tips": _ASSASSIN_BASE_TIPS
        + [
            "As the Marksman, you can hit up to three targets including players, creatures and/or"
            " planeswalkers. Creatures lose hexproof and shroud — combine with other spells.",
        ],
        "clarifications": [],
    },
    "The Priestess": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Exchange life totals, accumulated commander damage, and poison counters with target player."
            " | Activate only during your turn."
        ),
        "passive": None,
        "tips": _ASSASSIN_BASE_TIPS
        + [
            "As the Priestess, lure the King into a false sense of hope"
            " before draining his life in front of his allies.",
        ],
        "clarifications": [
            "Can only Announce during your turn.",
            "If an effect prevents a player from losing life, that player can't exchange life totals"
            " with a player who has a lower life total — the exchange won't happen.",
            "Exchanging commander damage also exchanges all commander damage received from each opponent.",
        ],
    },
    "The Schemer": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Choose one — During target player's next turn, you control that player during all"
            " combat phases; or during target player's next turn, you control that player"
            " during all non-combat phases."
            " | Activate only during your turn."
        ),
        "passive": None,
        "tips": _ASSASSIN_BASE_TIPS
        + [
            "As the Schemer, you've dreamed of revenge for years."
            " Control the King's turn at the perfect moment to deal the killing blow.",
        ],
        "clarifications": [
            "Can only Announce during your turn.",
            "When controlling another player's phase, you may look at and cast spells from their hand.",
            "While controlling another player, you make all choices that player is allowed or told to make"
            " — spells to cast, abilities to activate, and any triggered ability decisions.",
        ],
    },
    "The Thief": {
        "role": "Assassin",
        "life": None,
        "victory": "The King is eliminated.",
        "defeat": None,
        "announce": (
            "Untap target permanent and gain control of it until the beginning of your next end step."
            " It gains haste until end of turn."
        ),
        "passive": None,
        "tips": _ASSASSIN_BASE_TIPS
        + [
            "As the Thief, you gain control until the beginning of your next end step"
            " — longer than a standard 'until end of turn'. Use the stolen permanent on your turn"
            " and keep it through your opponents' turns.",
        ],
        "clarifications": [
            "Control lasts until the beginning of your next end step, not until end of turn.",
        ],
    },
    # ── Bandits ───────────────────────────────────────────────────────────────
    "The Giant": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Choose one creature with the highest combined power and toughness. Destroy the rest."
            " | Activate only during your turn."
        ),
        "passive": None,
        "tips": _BANDIT_BASE_TIPS
        + [
            "As the Giant, wait for the perfect moment to clear the board."
            " If multiple creatures are tied for the highest combined power and toughness,"
            " you choose which one survives.",
        ],
        "clarifications": [
            "Can only Announce during your turn.",
            "If multiple creatures are tied for the highest combined power and toughness,"
            " you choose which of those will not be destroyed.",
        ],
    },
    "The Necromancer": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Target opponent with a face up role card mills ten cards."
            " Exile all creature cards from that player's graveyard."
            " That player separates those cards into two piles."
            " Put all cards from the pile of your choice onto the battlefield under your control"
            " and exile the rest."
            " Until the end of your next turn, those creatures gain indestructible."
        ),
        "passive": None,
        "tips": _BANDIT_BASE_TIPS
        + [
            "As the Necromancer, mill your target first to fill their graveyard,"
            " then steal their best creatures — now indestructible until your next turn.",
        ],
        "clarifications": [
            "An opponent with a face up Role card separates the creatures into piles."
            " Your Bandit teammate cannot pick your piles.",
            "Piles may be empty.",
            "If no opponents have face up Role cards, the Necromancer cannot Announce.",
        ],
    },
    "The Stalker": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Split Second. Exile target permanent."
            " (As long as this ability is on the stack, players can't cast spells"
            " or activate abilities that aren't mana abilities.)"
        ),
        "passive": None,
        "tips": _BANDIT_BASE_TIPS
        + [
            "As the Stalker, Split Second means your Announce cannot be responded to with spells or"
            " non-mana abilities. Spring from the darkness — give your enemies no time to react.",
        ],
        "clarifications": [
            "Players still get priority while Split Second is on the stack; options are limited"
            " to mana abilities and certain special actions.",
            "After the Split Second ability resolves, players may again cast spells and activate"
            " abilities before the next object on the stack resolves.",
        ],
    },
    "The Wizard": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Choose one — Exile target spell;"
            " or change the target of target spell or ability."
            " (Role abilities cannot be targeted.)"
        ),
        "passive": None,
        "tips": _BANDIT_BASE_TIPS
        + [
            "As the Wizard, an exiled spell isn't countered but it won't resolve —"
            " this works against spells that can't be countered.",
        ],
        "clarifications": [
            "You may only choose one of the two options upon Announcing.",
            "An exiled spell isn't countered, but it won't resolve.",
            "You don't choose the new target for the spell or ability until this ability resolves.",
            "You can't change the target to an illegal target. Role abilities cannot be targeted.",
        ],
    },
    "The Zealot": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Each player with a face up role card exiles cards from the top of their library"
            " until they reveal a creature card with mana value 4 or greater."
            " For each creature card revealed this way, you may put that card onto the"
            " battlefield under your control."
            " Shuffle all cards not put onto the battlefield this way into their owners' libraries."
            " Those creatures gain vigilance, haste, and double strike until end of turn."
        ),
        "passive": None,
        "tips": _BANDIT_BASE_TIPS
        + [
            "As the Zealot, only creature cards with mana value 4 or greater enter the battlefield."
            " Build your deck around powerful high-cost creatures to maximise this ability.",
        ],
        "clarifications": [
            "A 'creature card' is any card with the type creature, including artifact creatures and lands.",
            "If no creatures with mana value 4 or greater exist in a player's library, all cards are"
            " exiled from that library, then shuffled back in.",
            "Only revealed creatures with mana value 4 or greater enter the battlefield under the Zealot's"
            " control. All other exiled creatures are shuffled back into their owner's libraries.",
        ],
    },
    # ── Renegades ─────────────────────────────────────────────────────────────
    "The Champion": {
        "role": "Renegade",
        "life": None,
        "victory": "The Challenger is eliminated.",
        "defeat": None,
        "announce": (
            "Triggered when any player has 25 or less life — Choose a non-King"
            " opponent with the highest life total at random to become the Challenger."
        ),
        "passive": "At the beginning of your upkeep, Scry 1.",
        "tips": [
            "Renegades are the wild cards of the kingdom. Each character has unique motivations.",
            "As the Champion, maintain a high life total while reducing all opponents' life totals"
            " equally — you want to be at an advantage when the Challenger is revealed.",
            "The Champion only wins if the Challenger is eliminated, regardless of who did it.",
            "Your opponents won't know your victory condition until you Announce. Use this to set up"
            " an optimal board state beforehand.",
        ],
        "clarifications": [
            "When a player has 25 or less life for the first time, the Champion is required to Announce"
            " as a triggered ability.",
            "The Champion only wins if the Challenger is eliminated."
            " It does not matter who was responsible.",
        ],
    },
    "The Cultist": {
        "role": "Renegade",
        "life": None,
        "victory": (
            "At least half of the starting number of players in the game have Cultist Role cards."
        ),
        "defeat": None,
        "announce": (
            "Triggered when you would eliminate an opponent — instead, that player's role card"
            " becomes a copy of the Cultist"
            " (except it still has the type King if they were the King)."
            " Remove all commander damage and poison counters from that player."
            " Their life total becomes 15."
        ),
        "passive": None,
        "tips": [
            "Renegades are the wild cards of the kingdom. Each character has unique motivations.",
            "As the Cultist, instead of eliminating opponents you convert them to your cause.",
            "You win if at least half the starting player count are living Cultists.",
            "If a King is converted, the kingdom has no King — Knights lose their win condition and"
            " Assassins can no longer win by eliminating the King.",
        ],
        "clarifications": [
            "A player 'eliminated' by the Cultist becomes a face up Cultist instead.",
            "Converted Kings still have the King type — but Assassins cannot win by eliminating them.",
            "If the King is converted, Knights no longer have allegiance to anyone."
            " Assassins must be the last living players to win.",
            "The Cultist wins if at least half of the starting number of players are now living Cultists.",
        ],
    },
    "The Mimic": {
        "role": "Renegade",
        "life": None,
        "victory": "All other players are eliminated.",
        "defeat": None,
        "announce": "Triggered when you have 20 or less life — draw two cards.",
        "passive": (
            "At the beginning of your upkeep, target player loses 1 life;"
            " another target player gains 1 life."
            " Whenever you and any opponent have the same life total, that opponent is eliminated."
        ),
        "tips": [
            "Renegades are the wild cards of the kingdom. Each character has unique motivations.",
            "As the Mimic, use your passive to manipulate life totals — any opponent who matches"
            " your life total is immediately eliminated.",
            "You must target two different players with your upkeep ability.",
            "When your life total hits 20 or less for the first time, Announce and draw two cards.",
        ],
        "clarifications": [
            "You are required to Announce when your life total becomes 20 or less for the first time.",
            "You draw two cards one time (i.e. when you Announce).",
            "You must target two different players with your upkeep ability.",
            "If at any point another player has the same life total as the Mimic,"
            " that player is immediately eliminated.",
        ],
    },
    "The Sellsword": {
        "role": "Renegade",
        "life": None,
        "victory": "Your teammate wins.",
        "defeat": "You or a teammate are eliminated.",
        "announce": (
            "Triggered when any opponent Announces — starting with that player, each opponent"
            " bids any amount of life in turn order. The bidding ends when the high bid stands."
            " The high bidder loses life equal to the high bid, rounded up."
            " You and that player each sacrifice a land. That player becomes your teammate."
        ),
        "passive": None,
        "tips": [
            "Renegades are the wild cards of the kingdom. Each character has unique motivations.",
            "As the Sellsword, you vow to fight for the highest bidder."
            " When an opponent Announces, you must also Announce immediately.",
            "If your teammate's role is face down, follow their lead until you learn their win condition.",
            "If the Sellsword becomes teammates with a player who already has teammates (e.g. face up Bandits),"
            " all players are considered teammates.",
        ],
        "clarifications": [
            "When the first opponent Announces, the Sellsword is required to Announce as a triggered ability.",
            "Once a teammate is assigned, the Sellsword loses if their teammate is eliminated.",
            "If the Sellsword becomes teammates with a player who already has teammates, all are teammates."
            " If any teammate dies, the Sellsword is immediately eliminated.",
            "If the Sellsword is eliminated, their teammate(s) are NOT immediately eliminated.",
        ],
    },
    "The Straw Man": {
        "role": "Renegade",
        "life": None,
        "victory": "You are the first person to be eliminated and another player eliminated you.",
        "defeat": None,
        "announce": (
            "Until your next turn, creatures your opponents control must attack you if able."
            " At the beginning of your next upkeep, you have a replacement Victory condition:"
            " Victory — All other players are eliminated."
            " | Activate only on your turn."
        ),
        "passive": None,
        "tips": [
            "Renegades are the wild cards of the kingdom. Each character has unique motivations.",
            "As the Straw Man, only death can release you from your affliction."
            " Be political and unpredictable — make others want to eliminate you.",
            "Time your Announce wisely: too early and there aren't enough threats to finish the job;"
            " too late and another player may be eliminated before you.",
            "If another player is eliminated before you Announce, your initial victory condition becomes"
            " unachievable — but your Announce ability still works for the replacement condition.",
        ],
        "clarifications": [
            "The Announce ability affects all creatures opponents control,"
            " including any that enter the battlefield after the ability resolves.",
            "At the beginning of your next upkeep after Announcing, you gain the replacement victory condition.",
            "To eliminate yourself, you must control the effect responsible for eliminating you.",
        ],
    },
}

# ---------------------------------------------------------------------------
# Public variant descriptor
# ---------------------------------------------------------------------------

VARIANT: dict = {
    "id": VARIANT_ID,
    "name": "Advanced Kingdoms v2.0",
    "description": (
        "Latest ruleset (5–9 players). Updated characters, Split Second Stalker,"
        " Zealot targets MV 4+, and the Beloved Kings expansion included."
    ),
    "characters": _CHARACTERS,
    "distributions": _DISTRIBUTIONS,
}
