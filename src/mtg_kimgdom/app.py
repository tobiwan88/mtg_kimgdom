"""Flask web application for MTG Advanced Kingdoms.

Routes
------
GET  /                          Home — create-game form.
POST /create                    Process form; redirect host to share view.
GET  /game/<game_id>/share/<token>
                                Host share-link + character reveal page.
GET  /join/<game_id>            Join-game form.
POST /join/<game_id>            Process join; redirect player to role view.
GET  /play/<game_id>/<token>    Player character view.
GET  /api/status/<game_id>      JSON status (player list, lock state).
"""

import uuid

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from mtg_kimgdom.game import (
    CHARACTERS,
    MAX_PLAYERS,
    MIN_PLAYERS,
    ROLE_STYLES,
    make_distribution,
)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# In-memory game store
#
# games[game_id] = {
#     "total":      int,
#     "locked":     bool,
#     "players":    [{"name": str, "character": str, "token": str}, ...],
#     "card_pool":  [str, ...],   # remaining character names to be assigned
# }
# ---------------------------------------------------------------------------
games: dict[str, dict] = {}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _get_game_or_404(game_id: str) -> dict:
    """Return the game dict for *game_id*, or abort with 404."""
    game = games.get(game_id)
    if game is None:
        abort(404)
    return game


def _get_player_or_403(game: dict, token: str) -> dict:
    """Return the player dict matching *token*, or abort with 403."""
    player = next((p for p in game["players"] if p["token"] == token), None)
    if player is None:
        abort(403)
    return player


def _player_list_info(game: dict) -> list[dict]:
    """Return a public-safe list of player dicts (name + is_king only)."""
    return [
        {
            "name": p["name"],
            "is_king": CHARACTERS[p["character"]]["role"] == "King",
        }
        for p in game["players"]
    ]


def _bandit_teammates(game: dict, token: str) -> list[dict] | None:
    """Return fellow Bandits (name + character) for a Bandit player, or None."""
    player = next(p for p in game["players"] if p["token"] == token)
    if CHARACTERS[player["character"]]["role"] != "Bandit":
        return None
    return [
        {"name": p["name"], "character": p["character"]}
        for p in game["players"]
        if CHARACTERS[p["character"]]["role"] == "Bandit" and p["token"] != token
    ]


def _card_context(character_name: str) -> dict:
    """Return the merged template context dict for one character card."""
    char = CHARACTERS[character_name]
    style = ROLE_STYLES[char["role"]]
    return {
        "character_name": character_name,
        "character": char,
        "role_type": char["role"],
        "style": style,
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    """Render the create-game form."""
    return render_template(
        "index.html",
        error=None,
        min_players=MIN_PLAYERS,
        max_players=MAX_PLAYERS,
    )


@app.route("/create", methods=["POST"])
def create():
    """Validate form data, create a new game, redirect host to share view."""
    name = request.form.get("name", "").strip()
    total_raw = request.form.get("total", "").strip()

    if not name:
        return render_template(
            "index.html",
            error="Please enter your name.",
            min_players=MIN_PLAYERS,
            max_players=MAX_PLAYERS,
        )

    try:
        total = int(total_raw)
        if not (MIN_PLAYERS <= total <= MAX_PLAYERS):
            raise ValueError
    except ValueError:
        return render_template(
            "index.html",
            error=(f"Player count must be between {MIN_PLAYERS} and {MAX_PLAYERS}."),
            min_players=MIN_PLAYERS,
            max_players=MAX_PLAYERS,
        )

    game_id = uuid.uuid4().hex[:10]
    cards = make_distribution(total)
    host_token = uuid.uuid4().hex

    games[game_id] = {
        "total": total,
        "locked": False,
        "players": [{"name": name, "character": cards[0], "token": host_token}],
        "card_pool": cards[1:],
    }

    return redirect(url_for("share", game_id=game_id, token=host_token))


@app.route("/game/<game_id>/share/<token>")
def share(game_id: str, token: str):
    """Show the host their character card and the shareable join link."""
    game = _get_game_or_404(game_id)
    player = _get_player_or_403(game, token)

    join_url = request.host_url.rstrip("/") + url_for("join", game_id=game_id)

    return render_template(
        "share.html",
        game_id=game_id,
        **_card_context(player["character"]),
        join_url=join_url,
        joined=len(game["players"]),
        total=game["total"],
    )


@app.route("/join/<game_id>", methods=["GET", "POST"])
def join(game_id: str):
    """Display the join form (GET) or process a player joining (POST)."""
    game = _get_game_or_404(game_id)

    joined = len(game["players"])
    total = game["total"]
    locked = game["locked"]

    if request.method == "GET":
        return render_template(
            "join.html",
            error=None,
            locked=locked,
            joined=joined,
            total=total,
        )

    # POST ----------------------------------------------------------------
    if locked:
        return render_template(
            "join.html",
            error=None,
            locked=True,
            joined=joined,
            total=total,
        )

    name = request.form.get("name", "").strip()
    if not name:
        return render_template(
            "join.html",
            error="Please enter your name.",
            locked=False,
            joined=joined,
            total=total,
        )

    pool = game["card_pool"]
    if not pool:
        game["locked"] = True
        return render_template(
            "join.html",
            error=None,
            locked=True,
            joined=joined,
            total=total,
        )

    character_name = pool.pop(0)
    token = uuid.uuid4().hex
    game["players"].append({"name": name, "character": character_name, "token": token})

    if len(game["players"]) >= game["total"]:
        game["locked"] = True

    return redirect(url_for("player_view", game_id=game_id, token=token))


@app.route("/play/<game_id>/<token>")
def player_view(game_id: str, token: str):
    """Show a player their secret character card and the live player list."""
    game = _get_game_or_404(game_id)
    player = _get_player_or_403(game, token)

    return render_template(
        "role.html",
        game_id=game_id,
        player_name=player["name"],
        **_card_context(player["character"]),
        players=_player_list_info(game),
        bandit_teammates=_bandit_teammates(game, token),
        joined=len(game["players"]),
        total=game["total"],
        locked=game["locked"],
    )


@app.route("/api/status/<game_id>")
def api_status(game_id: str):
    """Return JSON with current player list and lock state."""
    game = _get_game_or_404(game_id)

    return jsonify(
        joined=len(game["players"]),
        total=game["total"],
        locked=game["locked"],
        players=_player_list_info(game),
    )
