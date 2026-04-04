import uuid
import random
from flask import Flask, request, redirect, url_for, render_template_string, abort

app = Flask(__name__)

# ─── In-memory store ────────────────────────────────────────────────────────
# games[game_id] = {
#   "total": int,
#   "players": [ {"name": str, "role": str, "token": str}, ... ],
#   "locked": bool,
# }
games: dict = {}

# ─── Role data ───────────────────────────────────────────────────────────────
ROLES = {
    "King": {
        "color": "#FFD700",
        "border": "#b8860b",
        "icon": "👑",
        "team": "Royal",
        "public": True,
        "life": 50,
        "description": (
            "Your identity is revealed to all players at the start of the game. "
            "You begin with <strong>50 life</strong> instead of 40."
        ),
        "win": "Win if only you and your Knights remain alive.",
    },
    "Knight": {
        "color": "#4FC3F7",
        "border": "#0288d1",
        "icon": "⚔️",
        "team": "Royal",
        "public": False,
        "description": "You serve the King. Keep your role hidden.",
        "win": (
            "Win alongside the King if all Assassins, Bandits, and Renegades "
            "are eliminated."
        ),
    },
    "Assassin": {
        "color": "#EF5350",
        "border": "#b71c1c",
        "icon": "🗡️",
        "team": "Assassins",
        "public": False,
        "description": "You seek the King's head. Keep your role hidden.",
        "win": (
            "Win by being the last player standing. "
            "You must outlive all Bandits — if a Bandit is alive when the King dies, "
            "the Bandits win instead."
        ),
    },
    "Bandit": {
        "color": "#AB47BC",
        "border": "#6a1b9a",
        "icon": "💀",
        "team": "Bandits",
        "public": False,
        "description": "You scheme against the King. Keep your role hidden.",
        "win": (
            "Win if at least one Bandit is still alive when the King is eliminated."
        ),
    },
    "Renegade": {
        "color": "#66BB6A",
        "border": "#2e7d32",
        "icon": "🌀",
        "team": "None",
        "public": False,
        "description": "You walk alone. Keep your role hidden.",
        "win": "Win by being the very last player standing.",
    },
}

# ─── Role distribution ───────────────────────────────────────────────────────
DISTRIBUTIONS = {
    3:  ["King", "Assassin", "Bandit"],
    4:  ["King", "Knight", "Assassin", "Bandit"],
    5:  ["King", "Knight", "Assassin", "Bandit", "Renegade"],
    6:  ["King", "Knight", "Knight", "Assassin", "Bandit", "Renegade"],
    7:  ["King", "Knight", "Knight", "Assassin", "Assassin", "Bandit", "Renegade"],
    8:  ["King", "Knight", "Knight", "Assassin", "Assassin", "Bandit", "Bandit", "Renegade"],
    9:  ["King", "Knight", "Knight", "Knight", "Assassin", "Assassin", "Bandit", "Bandit", "Renegade"],
    10: ["King", "Knight", "Knight", "Knight", "Assassin", "Assassin", "Bandit", "Bandit", "Renegade", "Renegade"],
}

def make_distribution(n: int) -> list[str]:
    if n in DISTRIBUTIONS:
        roles = DISTRIBUTIONS[n][:]
    elif n > 10:
        # Scale up: add Knights and Assassins evenly
        base = DISTRIBUTIONS[10][:]
        extra = n - 10
        for i in range(extra):
            base.append("Knight" if i % 2 == 0 else "Assassin")
        roles = base
    else:
        roles = DISTRIBUTIONS[3][:]
    random.shuffle(roles)
    return roles


# ─── Templates ───────────────────────────────────────────────────────────────
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
    font-family: 'Georgia', serif;
    background: #0d0d0d;
    color: #e8d5a3;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1rem;
}
.card {
    background: #1a1208;
    border: 2px solid #5a4010;
    border-radius: 12px;
    padding: 2rem;
    max-width: 520px;
    width: 100%;
    box-shadow: 0 0 40px rgba(180, 120, 0, 0.15);
}
h1 { font-size: 1.8rem; color: #FFD700; margin-bottom: 0.3rem; text-align: center; }
h2 { font-size: 1.3rem; color: #FFD700; margin-bottom: 1rem; text-align: center; }
.subtitle { text-align: center; color: #a08840; font-size: 0.9rem; margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.3rem; color: #c9a84c; font-size: 0.9rem; }
input[type=text], input[type=number] {
    width: 100%;
    padding: 0.65rem 0.9rem;
    border-radius: 7px;
    border: 1px solid #5a4010;
    background: #0d0d0d;
    color: #e8d5a3;
    font-size: 1rem;
    margin-bottom: 1rem;
    font-family: inherit;
}
input:focus { outline: none; border-color: #FFD700; }
button {
    width: 100%;
    padding: 0.75rem;
    border-radius: 8px;
    border: none;
    background: linear-gradient(135deg, #b8860b, #FFD700);
    color: #0d0d0d;
    font-size: 1.05rem;
    font-weight: bold;
    cursor: pointer;
    font-family: inherit;
    letter-spacing: 0.03em;
    transition: opacity 0.2s;
}
button:hover { opacity: 0.88; }
.error { color: #EF5350; font-size: 0.9rem; margin-bottom: 1rem; text-align: center; }
.divider { border: none; border-top: 1px solid #3a2a08; margin: 1.2rem 0; }
a { color: #FFD700; }
"""

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MTG Commander Kingdom</title>
  <style>{{ css }}</style>
</head>
<body>
  <div class="card">
    <h1>⚔️ Commander Kingdom</h1>
    <p class="subtitle">Advanced Kingdoms — EDH Variant</p>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    <form method="POST" action="/create">
      <label for="name">Your name</label>
      <input type="text" id="name" name="name" placeholder="e.g. Gandalf" required maxlength="30" autocomplete="off">
      <label for="total">Number of players (3–12)</label>
      <input type="number" id="total" name="total" min="3" max="12" value="5" required>
      <button type="submit">Create Game &amp; Get My Role</button>
    </form>
  </div>
</body>
</html>
"""

SHARE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Game Created — Commander Kingdom</title>
  <style>
    {{ css }}
    .share-box {
        background: #0d0d0d;
        border: 1px dashed #5a4010;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        font-size: 0.85rem;
        color: #c9a84c;
        word-break: break-all;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: border-color 0.2s;
    }
    .share-box:hover { border-color: #FFD700; }
    .copied-msg { display: none; color: #66BB6A; font-size: 0.85rem; text-align: center; margin-top: -0.5rem; margin-bottom: 0.8rem; }
    .role-card {
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        border: 2px solid {{ role.border }};
        background: #0a0a0a;
    }
    .role-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.7rem;
    }
    .role-icon { font-size: 2rem; }
    .role-name { font-size: 1.5rem; font-weight: bold; color: {{ role.color }}; }
    .role-team { font-size: 0.78rem; color: #a08840; text-transform: uppercase; letter-spacing: 0.08em; }
    .role-desc, .role-win { font-size: 0.9rem; line-height: 1.5; color: #c9a84c; }
    .role-win { margin-top: 0.6rem; color: #e8d5a3; }
    .badge-public {
        display: inline-block;
        background: #FFD700;
        color: #0d0d0d;
        font-size: 0.72rem;
        font-weight: bold;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    .waiting { text-align: center; color: #a08840; font-size: 0.9rem; margin-top: 0.8rem; }
    .waiting strong { color: #FFD700; }
  </style>
  <script>
    function copyLink() {
      navigator.clipboard.writeText(document.getElementById('join-url').textContent.trim());
      document.getElementById('copied').style.display = 'block';
      setTimeout(() => document.getElementById('copied').style.display = 'none', 2000);
    }
    // Auto-refresh waiting count
    function refreshCount() {
      fetch('/api/status/{{ game_id }}')
        .then(r => r.json())
        .then(d => {
          document.getElementById('joined-count').textContent = d.joined;
          document.getElementById('total-count').textContent = d.total;
          if (d.locked) {
            document.getElementById('waiting-msg').innerHTML =
              '<strong>All players have joined!</strong> The game is locked.';
          }
        });
    }
    setInterval(refreshCount, 3000);
  </script>
</head>
<body>
  <div class="card">
    <h1>⚔️ Commander Kingdom</h1>
    <h2>Your Secret Role</h2>

    <div class="role-card">
      <div class="role-header">
        <span class="role-icon">{{ role.icon }}</span>
        <div>
          <span class="role-name">{{ role_name }}</span>
          {% if role.public %}<span class="badge-public">PUBLIC</span>{% endif %}
          <div class="role-team">{{ role.team }}</div>
        </div>
      </div>
      <p class="role-desc">{{ role.description | safe }}</p>
      <p class="role-win"><strong>Victory:</strong> {{ role.win }}</p>
      {% if role.life %}
      <p class="role-win" style="margin-top:0.4rem;"><strong>Starting life:</strong> {{ role.life }}</p>
      {% endif %}
    </div>

    <hr class="divider">
    <p style="font-size:0.9rem; color:#a08840; margin-bottom:0.5rem;">Share this link with other players:</p>
    <div class="share-box" onclick="copyLink()" title="Click to copy">
      <span id="join-url">{{ join_url }}</span>
    </div>
    <p class="copied-msg" id="copied">✓ Copied to clipboard!</p>

    <div class="waiting" id="waiting-msg">
      Waiting for players…
      <strong id="joined-count">{{ joined }}</strong> /
      <strong id="total-count">{{ total }}</strong> joined
    </div>
  </div>
</body>
</html>
"""

JOIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Join — Commander Kingdom</title>
  <style>{{ css }}</style>
</head>
<body>
  <div class="card">
    <h1>⚔️ Commander Kingdom</h1>
    <p class="subtitle">Advanced Kingdoms — EDH Variant</p>
    {% if error %}<p class="error">{{ error }}</p>{% endif %}
    {% if locked %}
      <p class="error" style="font-size:1rem;">This game is full. No more players can join.</p>
    {% else %}
      <p style="font-size:0.9rem; color:#a08840; margin-bottom:1.2rem; text-align:center;">
        {{ joined }} / {{ total }} players have joined.
      </p>
      <form method="POST">
        <label for="name">Your name</label>
        <input type="text" id="name" name="name" placeholder="e.g. Aragorn" required maxlength="30" autocomplete="off">
        <button type="submit">Join &amp; Reveal My Role</button>
      </form>
    {% endif %}
  </div>
</body>
</html>
"""

ROLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Role — Commander Kingdom</title>
  <style>
    {{ css }}
    .role-card {
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1.2rem;
        border: 2px solid {{ role.border }};
        background: #0a0a0a;
    }
    .role-header {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin-bottom: 0.7rem;
    }
    .role-icon { font-size: 2rem; }
    .role-name { font-size: 1.5rem; font-weight: bold; color: {{ role.color }}; }
    .role-team { font-size: 0.78rem; color: #a08840; text-transform: uppercase; letter-spacing: 0.08em; }
    .role-desc, .role-win { font-size: 0.9rem; line-height: 1.5; color: #c9a84c; }
    .role-win { margin-top: 0.6rem; color: #e8d5a3; }
    .badge-public {
        display: inline-block;
        background: #FFD700;
        color: #0d0d0d;
        font-size: 0.72rem;
        font-weight: bold;
        padding: 0.15rem 0.5rem;
        border-radius: 4px;
        margin-left: 0.5rem;
        vertical-align: middle;
    }
    .player-name {
        text-align: center;
        color: #a08840;
        font-size: 0.95rem;
        margin-bottom: 1.2rem;
    }
    .player-name strong { color: #FFD700; }
    .players-list {
        margin-top: 1rem;
    }
    .players-list h3 { font-size: 0.9rem; color: #a08840; margin-bottom: 0.6rem; text-transform: uppercase; letter-spacing: 0.06em; }
    .player-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.35rem 0;
        font-size: 0.9rem;
        border-bottom: 1px solid #2a1e08;
        color: #c9a84c;
    }
    .player-item:last-child { border-bottom: none; }
    .dot { width: 8px; height: 8px; border-radius: 50%; background: #5a4010; flex-shrink: 0; }
    .dot.king { background: #FFD700; }
    .status { text-align: center; margin-top: 1rem; font-size: 0.85rem; color: #a08840; }
  </style>
  <script>
    // Refresh player list
    function refreshPlayers() {
      fetch('/api/status/{{ game_id }}')
        .then(r => r.json())
        .then(d => {
          const list = document.getElementById('player-list');
          list.innerHTML = d.players.map(p =>
            '<div class="player-item">' +
            '<span class="dot' + (p.is_king ? ' king' : '') + '"></span>' +
            p.name + (p.is_king ? ' 👑' : '') +
            '</div>'
          ).join('');
          document.getElementById('status-msg').textContent =
            d.locked
              ? 'All ' + d.total + ' players have joined. Game on!'
              : d.joined + ' / ' + d.total + ' players joined…';
        });
    }
    setInterval(refreshPlayers, 3000);
  </script>
</head>
<body>
  <div class="card">
    <h1>⚔️ Commander Kingdom</h1>
    <p class="player-name">Playing as <strong>{{ player_name }}</strong></p>

    <div class="role-card">
      <div class="role-header">
        <span class="role-icon">{{ role.icon }}</span>
        <div>
          <span class="role-name">{{ role_name }}</span>
          {% if role.public %}<span class="badge-public">PUBLIC</span>{% endif %}
          <div class="role-team">{{ role.team }}</div>
        </div>
      </div>
      <p class="role-desc">{{ role.description | safe }}</p>
      <p class="role-win"><strong>Victory:</strong> {{ role.win }}</p>
      {% if role.life %}
      <p class="role-win" style="margin-top:0.4rem;"><strong>Starting life:</strong> {{ role.life }}</p>
      {% endif %}
    </div>

    <div class="players-list">
      <h3>Players in this game</h3>
      <div id="player-list">
        {% for p in players %}
        <div class="player-item">
          <span class="dot {% if p.is_king %}king{% endif %}"></span>
          {{ p.name }}{% if p.is_king %} 👑{% endif %}
        </div>
        {% endfor %}
      </div>
      <p class="status" id="status-msg">
        {% if locked %}All {{ total }} players have joined. Game on!
        {% else %}{{ joined }} / {{ total }} players joined…{% endif %}
      </p>
    </div>
  </div>
</body>
</html>
"""


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HOME_TEMPLATE, css=BASE_CSS, error=None)


@app.route("/create", methods=["POST"])
def create():
    name = request.form.get("name", "").strip()
    total_str = request.form.get("total", "").strip()

    if not name:
        return render_template_string(HOME_TEMPLATE, css=BASE_CSS, error="Please enter your name.")

    try:
        total = int(total_str)
        if not (3 <= total <= 12):
            raise ValueError
    except ValueError:
        return render_template_string(HOME_TEMPLATE, css=BASE_CSS, error="Player count must be between 3 and 12.")

    game_id = uuid.uuid4().hex[:10]
    roles = make_distribution(total)
    host_token = uuid.uuid4().hex

    games[game_id] = {
        "total": total,
        "locked": False,
        "players": [{"name": name, "role": roles[0], "token": host_token}],
        "_roles_pool": roles[1:],  # remaining roles for joiners
    }

    return redirect(url_for("share", game_id=game_id, token=host_token))


@app.route("/game/<game_id>/share/<token>")
def share(game_id, token):
    game = games.get(game_id)
    if not game:
        abort(404)

    player = next((p for p in game["players"] if p["token"] == token), None)
    if not player:
        abort(403)

    role = ROLES[player["role"]]
    join_url = request.host_url.rstrip("/") + f"/join/{game_id}"
    joined = len(game["players"])
    total = game["total"]

    return render_template_string(
        SHARE_TEMPLATE,
        css=BASE_CSS,
        game_id=game_id,
        role=role,
        role_name=player["role"],
        join_url=join_url,
        joined=joined,
        total=total,
    )


@app.route("/join/<game_id>", methods=["GET", "POST"])
def join(game_id):
    game = games.get(game_id)
    if not game:
        abort(404)

    joined = len(game["players"])
    total = game["total"]
    locked = game["locked"]

    if request.method == "GET":
        return render_template_string(
            JOIN_TEMPLATE,
            css=BASE_CSS,
            error=None,
            locked=locked,
            joined=joined,
            total=total,
        )

    # POST — join the game
    if locked:
        return render_template_string(
            JOIN_TEMPLATE,
            css=BASE_CSS,
            error=None,
            locked=True,
            joined=joined,
            total=total,
        )

    name = request.form.get("name", "").strip()
    if not name:
        return render_template_string(
            JOIN_TEMPLATE,
            css=BASE_CSS,
            error="Please enter your name.",
            locked=False,
            joined=joined,
            total=total,
        )

    # Assign next role from pool
    pool = game["_roles_pool"]
    if not pool:
        game["locked"] = True
        return render_template_string(
            JOIN_TEMPLATE,
            css=BASE_CSS,
            error=None,
            locked=True,
            joined=joined,
            total=total,
        )

    role_name = pool.pop(0)
    token = uuid.uuid4().hex
    game["players"].append({"name": name, "role": role_name, "token": token})

    # Lock if now full
    if len(game["players"]) >= game["total"]:
        game["locked"] = True

    return redirect(url_for("player_view", game_id=game_id, token=token))


@app.route("/play/<game_id>/<token>")
def player_view(game_id, token):
    game = games.get(game_id)
    if not game:
        abort(404)

    player = next((p for p in game["players"] if p["token"] == token), None)
    if not player:
        abort(403)

    role = ROLES[player["role"]]
    players_info = [
        {
            "name": p["name"],
            "is_king": p["role"] == "King",
        }
        for p in game["players"]
    ]

    return render_template_string(
        ROLE_TEMPLATE,
        css=BASE_CSS,
        game_id=game_id,
        player_name=player["name"],
        role=role,
        role_name=player["role"],
        players=players_info,
        joined=len(game["players"]),
        total=game["total"],
        locked=game["locked"],
    )


@app.route("/api/status/<game_id>")
def api_status(game_id):
    game = games.get(game_id)
    if not game:
        abort(404)

    players_info = [
        {"name": p["name"], "is_king": p["role"] == "King"}
        for p in game["players"]
    ]

    from flask import jsonify
    return jsonify(
        joined=len(game["players"]),
        total=game["total"],
        locked=game["locked"],
        players=players_info,
    )


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
