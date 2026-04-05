# Requirements — MTG Commander Kingdom

Cross-reference of the Advanced Kingdoms v1.56 ruleset (PDF) against the current app.

---

## Game Setup

| # | Requirement | Status |
|---|-------------|--------|
| S1 | Support 5–9 players (official PDF distributions) | ✅ |
| S2 | Randomly select characters per role type per player count | ✅ |
| S3 | Deal one secret role card per player | ✅ |
| S4 | King role is always public — revealed to all players at start | ✅ |
| S5 | Bandits identify each other at game start (3+ Bandits only per PDF) | ⚠️ App shows bandit teammates for any bandit count (2 or 3); PDF specifies 3+ only |
| S6 | Assassins do **not** identify each other at start | ✅ Not shown |
| S7 | King starts with +10 life (50 total) | ✅ |

**Player count distributions (PDF Game Setup card):**

| Players | King | Knight | Assassin | Bandit | Renegade |
|---------|------|--------|----------|--------|----------|
| 5p | 1 | 1 | 2 | 0 | 1 |
| 6p | 1 | 1 | 2 | 2 | 0 |
| 7p | 1 | 1 | 2 | 2 | 1 |
| 8p | 1 | 1 | 3 | 2 | 1 |
| 9p | 1 | 2 | 3 | 3 | 0 |

> Note: README role table references 3–12 players with a different incremental distribution — this appears to be a separate variant not covered by the PDF setup card. Currently not implemented.

---

## Role Cards

### Display

| # | Requirement | Status |
|---|-------------|--------|
| R1 | Show character name and role type | ✅ |
| R2 | Show role icon and colour per role type | ✅ |
| R3 | Show Victory condition | ✅ |
| R4 | Show Defeat condition (or default "You are eliminated" if none) | ✅ |
| R5 | Show Announce ability text with timing note | ✅ |
| R6 | Show Passive ability text | ✅ |
| R7 | Show starting life override (King: 50) | ✅ |
| R8 | Show "PUBLIC" badge on King card | ✅ |
| R9 | Show Tips & Clarifications per role (shown on PDF tip cards) | ❌ Not implemented |

### Characters implemented

| Role | Character | Status |
|------|-----------|--------|
| King | The King | ✅ |
| Knight | The Field Marshal | ✅ |
| Knight | The Kingslayer | ✅ |
| Knight | The Knight in Shining Armor | ✅ |
| Knight | The Queen | ✅ |
| Knight | The Rightful Heir | ✅ |
| Assassin | The Bear Trainer | ✅ |
| Assassin | The Marksman | ✅ |
| Assassin | The Priestess | ✅ |
| Assassin | The Schemer | ✅ |
| Assassin | The Thief | ✅ |
| Renegade | The Champion | ✅ |
| Renegade | The Cultist | ✅ |
| Renegade | The Mimic | ✅ |
| Renegade | The Sellsword | ✅ |
| Renegade | The Straw Man | ✅ |
| Bandit | The Giant | ✅ |
| Bandit | The Necromancer | ✅ |
| Bandit | The Stalker | ✅ |
| Bandit | The Wizard | ✅ |
| Bandit | The Zealot | ✅ |

---

## Game Rules (Quick Rules reference card)

| # | Rule | Status |
|---|------|--------|
| Q1 | Role cards start face down; cannot show face-down cards; reveal on elimination | ✅ Shown in rules on join page |
| Q2 | Face-up same-role players are teammates; face-up Knights and Kings are teammates | ✅ Shown in rules |
| Q3 | Only win/lose by Victory/Defeat conditions on role cards | ✅ Shown in rules |
| Q4 | Non-role "win/lose the game" abilities have no effect | ✅ Shown in rules |
| Q5 | First to meet Victory condition wins; simultaneous = shared win | ✅ Shown in rules |
| Q6 | "[Role] are eliminated" means all of that role are gone, not that you eliminated them | ✅ Shown in rules |
| Q7 | Defeat condition met = immediately eliminated | ✅ Shown in rules |
| Q8 | No Defeat condition = default "You are eliminated" | ✅ Shown in rules |
| Q9 | Possible to be eliminated and still win (e.g. Knight when King wins) | ✅ Shown in rules |
| Q10 | Announce = flip face-down card face up to activate ability; can't Announce twice | ✅ Shown in rules |
| Q11 | Role abilities use the stack; cannot be targeted, countered, or exiled | ✅ Shown in rules |
| Q12 | Taking control of a turn: can't look at their face-down role, they can't Announce | ✅ Shown in rules |
| Q13 | Empty library draw elimination: player who forced the draw 'eliminated' them | ✅ Shown in rules |
| Q14 | Kept alive through empty library draw: may shuffle graveyard/exile/hand into library | ✅ Shown in rules |
| Q15 | You 'eliminate' a player if your effect caused them to lose the game | ✅ Shown in rules |

---

## In-Game Tracking (not implemented)

These are gameplay mechanics that the app currently has no tracking for. All are handled at the physical table.

| # | Feature | Status |
|---|---------|--------|
| T1 | Mark a player as eliminated | ❌ |
| T2 | Track life totals | ❌ |
| T3 | Mark a role card as Announced (flipped face up) | ❌ |
| T4 | Track win condition met / declare winner | ❌ |
| T5 | Role card changes at runtime (e.g. Kingslayer transfers King, Cultist converts) | ❌ |
| T6 | Game log / event history | ❌ |

---

## Infrastructure

| # | Requirement | Status |
|---|-------------|--------|
| I1 | Join via shared link (no account needed) | ✅ |
| I2 | Each player sees only their own role | ✅ |
| I3 | Real-time player list (polling) | ✅ |
| I4 | Game locks when all players have joined | ✅ |
| I5 | Host share page with copyable join URL | ✅ |
| I6 | Game state persists across page refreshes (within session) | ✅ |
| I7 | Game state is in-memory — resets on server restart | ⚠️ Documented limitation |
| I8 | Persistent storage across restarts | ❌ |
