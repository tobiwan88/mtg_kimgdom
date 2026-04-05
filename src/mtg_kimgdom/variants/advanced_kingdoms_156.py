"""Advanced Kingdoms v1.56 variant — classic ruleset (3–12 players).

Character pool
--------------
King     : The King
Knights  : The Field Marshal, The Kingslayer, The Knight in Shining Armor,
           The Queen, The Rightful Heir
Assassins: The Bear Trainer, The Marksman, The Priestess, The Schemer, The Thief
Renegades: The Champion, The Cultist, The Mimic, The Sellsword, The Straw Man
Bandits  : The Giant, The Necromancer, The Stalker, The Wizard, The Zealot
"""

VARIANT_ID = "advanced_kingdoms_156"

# ---------------------------------------------------------------------------
# Player distributions (3–12 players)
# ---------------------------------------------------------------------------

_DISTRIBUTIONS: dict[int, dict[str, int]] = {
    3: {"King": 1, "Knight": 0, "Assassin": 1, "Bandit": 1, "Renegade": 0},
    4: {"King": 1, "Knight": 1, "Assassin": 1, "Bandit": 1, "Renegade": 0},
    5: {"King": 1, "Knight": 1, "Assassin": 1, "Bandit": 1, "Renegade": 1},
    6: {"King": 1, "Knight": 2, "Assassin": 1, "Bandit": 1, "Renegade": 1},
    7: {"King": 1, "Knight": 2, "Assassin": 2, "Bandit": 1, "Renegade": 1},
    8: {"King": 1, "Knight": 2, "Assassin": 2, "Bandit": 2, "Renegade": 1},
    9: {"King": 1, "Knight": 3, "Assassin": 2, "Bandit": 2, "Renegade": 1},
    10: {"King": 1, "Knight": 3, "Assassin": 2, "Bandit": 2, "Renegade": 2},
    11: {"King": 1, "Knight": 3, "Assassin": 3, "Bandit": 2, "Renegade": 2},
    12: {"King": 1, "Knight": 3, "Assassin": 3, "Bandit": 3, "Renegade": 2},
}

# ---------------------------------------------------------------------------
# Characters
# ---------------------------------------------------------------------------

_CHARACTERS: dict[str, dict] = {
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
        "tips": [
            "You are guaranteed to have a secret ally — a Knight — in your kingdom.",
            "Think twice before eliminating any face-down player. Eliminating your Knight"
            " will have severe consequences.",
            "Assassins will likely bluff as Knights in the early game. Be wary of small"
            " gestures made to gain your favor.",
            "Your alliance with the Bandits is temporary. They need you alive until the"
            " Assassins are gone — after that, they will turn on you.",
        ],
        "clarifications": [],
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
        "tips": [
            "Knights are the secret protectors of the kingdom. Serve your King well.",
            "You win by keeping your King alive and ridding the kingdom of all who seek"
            " to do him harm.",
            "As the Field Marshal, you are the King's battlefield expert. Help your King"
            " control the tide of war by confusing your enemies to fight amongst"
            " themselves during the heat of battle.",
            "Announce strategically and take advantage of the chaos after the ensuing battle.",
        ],
        "clarifications": [],
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
        "tips": [
            "Knights are the secret protectors of the kingdom. Serve your King well.",
            "You win by keeping your King alive and ridding the kingdom of all who seek"
            " to do him harm.",
            "As the Kingslayer, you have a backup plan if you find your King unfit to"
            " rule the kingdom.",
            "Remember: your primary objective is to protect the King. Turning against him"
            " should be considered a last resort when you see no other way to survive.",
        ],
        "clarifications": [
            "The King cannot choose the Kingslayer to be the new King.",
            "When a new King is chosen, the chosen player gains the King role card and"
            " discards their previous role card.",
        ],
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
        "tips": [
            "Knights are the secret protectors of the kingdom. Serve your King well.",
            "You win by keeping your King alive and ridding the kingdom of all who seek"
            " to do him harm.",
            "As the Knight in Shining Armor, your fighting skills are world renowned.",
            "It is rumored that your armor has never had as much as a scratch and shines"
            " so bright in the sunlight that it blinds your enemies.",
        ],
        "clarifications": [],
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
        "tips": [
            "Knights are the secret protectors of the kingdom. Serve your King well.",
            "You win by keeping your King alive and ridding the kingdom of all who seek"
            " to do him harm.",
            "As the Queen, you live to protect your King. Save his life by stalling his"
            " assailants while he heals his wounds.",
        ],
        "clarifications": [
            "You can only Announce if one of the following is true: the King is being"
            " attacked by unblocked creatures with total power ≥ the King's life total;"
            " dealt non-combat damage ≥ the King's life total; or attacked by an unblocked"
            " commander with power greater than the remaining commander-damage threshold.",
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
            " you gain the King role card and gain 10 life."
        ),
        "passive": None,
        "tips": [
            "Knights are the secret protectors of the kingdom. Serve your King well.",
            "You win by keeping your King alive and ridding the kingdom of all who seek"
            " to do him harm.",
            "As the Rightful Heir, you need to prove yourself worthy of the throne by"
            " eliminating one of your father's enemies.",
            "After doing so, if your father meets his tragic end, you will fulfill your"
            " birthright and take your place on the throne.",
        ],
        "clarifications": [
            "When you gain the King role card, discard the Rightful Heir role card.",
        ],
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
        "tips": [
            "Assassins have one task in mind: kill the King.",
            "You know there are more Assassins paid to help — unfortunately, you're not"
            " sure who they are.",
            "Your mission won't be easy. The King has a Knight hidden among you, and even"
            " Bandits and Renegades don't like drastic political change.",
            "As the Bear Trainer, you were once responsible for the bears in the King's"
            " army. Where the King saw them as disposable weapons, you knew they were"
            " much more. Now an outcast, you'll show the King their true power.",
        ],
        "clarifications": [],
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
        "tips": [
            "Assassins have one task in mind: kill the King.",
            "You know there are more Assassins paid to help — unfortunately, you're not"
            " sure who they are.",
            "Your mission won't be easy. The King has a Knight hidden among you, and even"
            " Bandits and Renegades don't like drastic political change.",
            "As the Marksman, you can hit any target within 100 metres. Work yourself"
            " within killing distance before taking the shot.",
        ],
        "clarifications": [],
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
        "tips": [
            "Assassins have one task in mind: kill the King.",
            "You know there are more Assassins paid to help — unfortunately, you're not"
            " sure who they are.",
            "Your mission won't be easy. The King has a Knight hidden among you, and even"
            " Bandits and Renegades don't like drastic political change.",
            "As the Priestess, you've studied the dark arts for years. Lure the King into"
            " a false sense of hope before draining his life in front of his allies.",
        ],
        "clarifications": [],
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
        "tips": [
            "Assassins have one task in mind: kill the King.",
            "You know there are more Assassins paid to help — unfortunately, you're not"
            " sure who they are.",
            "Your mission won't be easy. The King has a Knight hidden among you, and even"
            " Bandits and Renegades don't like drastic political change.",
            "As the Schemer, you've been waiting for this job for years — driven by revenge"
            " for your husband's unlawful execution by the King. Now is the time to act.",
        ],
        "clarifications": [
            "When controlling another player's phase, you may look at and cast spells"
            " from that player's hand.",
        ],
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
        "tips": [
            "Assassins have one task in mind: kill the King.",
            "You know there are more Assassins paid to help — unfortunately, you're not"
            " sure who they are.",
            "Your mission won't be easy. The King has a Knight hidden among you, and even"
            " Bandits and Renegades don't like drastic political change.",
            "As the Thief, you've never had problems getting your hands on what you want."
            " Take whatever you need to get the job done.",
        ],
        "clarifications": [],
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
        "tips": [
            "Renegades are the 'wild cards' of the kingdom. Each character has unique motivations.",
            "As the Champion, you've always been the best hand-to-hand combatant in the"
            " kingdom. You live to prove yourself in both tournaments and battle.",
            "You've heard rumours of a new challenger from a foreign land entering the"
            " upcoming tournament. Their identity remains cloaked in mystery.",
            "Once revealed, defend your title and dispose of the Challenger as quickly"
            " as possible.",
        ],
        "clarifications": [],
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
        "tips": [
            "Renegades are the 'wild cards' of the kingdom. Each character has unique motivations.",
            "As the Cultist, you seek to convert other players to join you. Once more"
            " than half of the players are Cultists, your following has enveloped the"
            " kingdom.",
        ],
        "clarifications": [
            "Converted Kings maintain their King type — Assassins do not instantly win"
            " if the Cultist converts a King.",
            "Knights no longer have allegiance to a converted King (he is now a Renegade)"
            " and do not lose when a Renegade King is eliminated.",
        ],
    },
    "The Mimic": {
        "role": "Renegade",
        "life": None,
        "victory": "All other players are eliminated.",
        "defeat": None,
        "announce": "Triggered when you have 20 or less life — draw a card.",
        "passive": (
            "At the beginning of your upkeep, target player loses 1 life;"
            " another target player gains 1 life. Whenever you and any"
            " opponent have the same life total, that opponent is eliminated."
        ),
        "tips": [
            "Renegades are the 'wild cards' of the kingdom. Each character has unique motivations.",
            "As the Mimic, you've never had a life of your own. You survive by taking"
            " over the lives of others.",
            "You are immortal, but these frail bodies decay over time. To survive, you"
            " must find other lives to devour.",
        ],
        "clarifications": [
            "If at any point another player has the same life total as the Mimic, that"
            " player is immediately eliminated.",
        ],
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
        "tips": [
            "Renegades are the 'wild cards' of the kingdom. Each character has unique motivations.",
            "As the Sellsword, you vow to fight for the highest bidder. See who can"
            " offer the largest payment and join their cause.",
            "If your teammate's role is face down, you won't know your new win condition."
            " Follow your teammate's lead.",
        ],
        "clarifications": [
            "After Announcing, the Sellsword retains their turn in turn order and does"
            " not share life totals or turns with their teammate.",
            "Once a teammate is assigned, the Sellsword loses the game when their"
            " teammate is eliminated.",
        ],
    },
    "The Straw Man": {
        "role": "Renegade",
        "life": None,
        "victory": "You are the first person to be eliminated and another player eliminated you.",
        "defeat": None,
        "announce": (
            "Until your next turn, all opponents' creatures must attack you if"
            " able. At the beginning of your next upkeep, you gain a"
            " replacement Victory condition: You eliminate yourself (loss of"
            " life, empty library, commander damage, or poison counters)."
            " | Activate only on your turn."
        ),
        "passive": None,
        "tips": [
            "Renegades are the 'wild cards' of the kingdom. Each character has unique motivations.",
            "As the Straw Man, you've been cursed to live a meaningless life. Only death"
            " will release you from this affliction.",
            "Be political. Do strange things. Make odd decisions. The less other players"
            " can trust you, the more likely they are to eliminate you.",
            "If your opponents don't finish the job, your replacement victory condition"
            " lets you find creative ways to end your own life.",
        ],
        "clarifications": [
            "To eliminate yourself, you must control the effect responsible for eliminating you.",
            "If you attempt to draw from an empty library, the player who forced you to"
            " draw (or who removed the last card) 'eliminated' you.",
        ],
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
        "tips": [
            "Contrary to popular belief, Bandits maintain balance within the kingdom."
            " Without Bandits, the King goes tyrannical — or Assassins murder the King"
            " and appoint a new leader of their own.",
            "Luckily, you have a Bandit teammate who is willing to help.",
            "Step 1 — Find and eliminate all Assassins trying to overthrow the King. You"
            " can't take down the monarchy until you've dealt with them first.",
            "Step 2 — Deal with the pesky Renegades, Knights, and King to install"
            " yourself on the throne.",
        ],
        "clarifications": [],
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
        "tips": [
            "Contrary to popular belief, Bandits maintain balance within the kingdom."
            " Without Bandits, the King goes tyrannical — or Assassins murder the King"
            " and appoint a new leader of their own.",
            "Luckily, you have a Bandit teammate who is willing to help.",
            "Step 1 — Find and eliminate all Assassins trying to overthrow the King. You"
            " can't take down the monarchy until you've dealt with them first.",
            "Step 2 — Deal with the pesky Renegades, Knights, and King to install"
            " yourself on the throne.",
        ],
        "clarifications": [],
    },
    "The Stalker": {
        "role": "Bandit",
        "life": None,
        "victory": "All non-Bandits are eliminated.",
        "defeat": "You or a teammate are eliminated.",
        "announce": "Exile target permanent.",
        "passive": None,
        "tips": [
            "Contrary to popular belief, Bandits maintain balance within the kingdom."
            " Without Bandits, the King goes tyrannical — or Assassins murder the King"
            " and appoint a new leader of their own.",
            "Luckily, you have a Bandit teammate who is willing to help.",
            "Step 1 — Find and eliminate all Assassins trying to overthrow the King. You"
            " can't take down the monarchy until you've dealt with them first.",
            "Step 2 — Deal with the pesky Renegades, Knights, and King to install"
            " yourself on the throne.",
        ],
        "clarifications": [],
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
        "tips": [
            "Contrary to popular belief, Bandits maintain balance within the kingdom."
            " Without Bandits, the King goes tyrannical — or Assassins murder the King"
            " and appoint a new leader of their own.",
            "Luckily, you have a Bandit teammate who is willing to help.",
            "Step 1 — Find and eliminate all Assassins trying to overthrow the King. You"
            " can't take down the monarchy until you've dealt with them first.",
            "Step 2 — Deal with the pesky Renegades, Knights, and King to install"
            " yourself on the throne.",
        ],
        "clarifications": [],
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
        "tips": [
            "Contrary to popular belief, Bandits maintain balance within the kingdom."
            " Without Bandits, the King goes tyrannical — or Assassins murder the King"
            " and appoint a new leader of their own.",
            "Luckily, you have a Bandit teammate who is willing to help.",
            "Step 1 — Find and eliminate all Assassins trying to overthrow the King. You"
            " can't take down the monarchy until you've dealt with them first.",
            "Step 2 — Deal with the pesky Renegades, Knights, and King to install"
            " yourself on the throne.",
        ],
        "clarifications": [],
    },
}

# ---------------------------------------------------------------------------
# Public variant descriptor
# ---------------------------------------------------------------------------

VARIANT: dict = {
    "id": VARIANT_ID,
    "name": "Advanced Kingdoms v1.56",
    "description": "The classic Advanced Kingdoms ruleset (3–12 players).",
    "characters": _CHARACTERS,
    "distributions": _DISTRIBUTIONS,
}
