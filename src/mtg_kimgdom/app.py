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

import os
import time
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
    DEFAULT_VARIANT,
    MAX_PLAYERS,
    MIN_PLAYERS,
    ROLE_STYLES,
    VARIANTS,
    make_distribution,
)

app = Flask(__name__)

MAX_SESSIONS = int(os.environ.get("MAX_SESSIONS", 20))
SESSION_TTL = 24 * 60 * 60  # 24 h in seconds

# ---------------------------------------------------------------------------
# In-memory game store
#
# games[game_id] = {
#     "total":      int,
#     "locked":     bool,
#     "created_at": float,        # time.time() at creation
#     "players":    [{"name": str, "character": str, "token": str}, ...],
#     "card_pool":  [str, ...],   # remaining character names to be assigned
# }
# ---------------------------------------------------------------------------
games: dict[str, dict] = {}


def _purge_sessions() -> None:
    """Remove sessions older than SESSION_TTL and enforce MAX_SESSIONS cap."""
    cutoff = time.time() - SESSION_TTL
    expired = [gid for gid, g in games.items() if g["created_at"] < cutoff]
    for gid in expired:
        del games[gid]

    while len(games) >= MAX_SESSIONS:
        oldest = min(games, key=lambda gid: games[gid]["created_at"])
        del games[oldest]


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
    characters = VARIANTS[game["variant"]]["characters"]
    return [
        {
            "name": p["name"],
            "is_king": characters[p["character"]]["role"] == "King",
        }
        for p in game["players"]
    ]


def _bandit_teammates(game: dict, token: str) -> list[dict] | None:
    """Return fellow Bandits (name + character) for a Bandit player, or None."""
    characters = VARIANTS[game["variant"]]["characters"]
    player = next(p for p in game["players"] if p["token"] == token)
    if characters[player["character"]]["role"] != "Bandit":
        return None
    return [
        {"name": p["name"], "character": p["character"]}
        for p in game["players"]
        if characters[p["character"]]["role"] == "Bandit" and p["token"] != token
    ]


def _card_context(character_name: str, variant_id: str = DEFAULT_VARIANT) -> dict:
    """Return the merged template context dict for one character card."""
    characters = VARIANTS[variant_id]["characters"]
    char = characters[character_name]
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
        variants=VARIANTS,
        default_variant=DEFAULT_VARIANT,
    )


def _index_error(error: str, variant_id: str = DEFAULT_VARIANT) -> str:
    """Render index.html with an error, preserving min/max for the chosen variant."""
    distributions = VARIANTS.get(variant_id, VARIANTS[DEFAULT_VARIANT])["distributions"]
    return render_template(
        "index.html",
        error=error,
        min_players=min(distributions),
        max_players=max(distributions),
        variants=VARIANTS,
        default_variant=variant_id,
    )


@app.route("/create", methods=["POST"])
def create():
    """Validate form data, create a new game, redirect host to share view."""
    name = request.form.get("name", "").strip()
    total_raw = request.form.get("total", "").strip()
    variant_id = request.form.get("variant", DEFAULT_VARIANT).strip()

    if variant_id not in VARIANTS:
        variant_id = DEFAULT_VARIANT

    if not name:
        return _index_error("Please enter your name.", variant_id)

    variant = VARIANTS[variant_id]
    distributions = variant["distributions"]
    min_p, max_p = min(distributions), max(distributions)

    try:
        total = int(total_raw)
        if total not in distributions:
            raise ValueError
    except ValueError:
        return _index_error(f"Player count must be between {min_p} and {max_p}.", variant_id)

    _purge_sessions()

    game_id = uuid.uuid4().hex[:10]
    cards = make_distribution(total, variant_id)
    host_token = uuid.uuid4().hex

    games[game_id] = {
        "total": total,
        "variant": variant_id,
        "locked": False,
        "created_at": time.time(),
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
        **_card_context(player["character"], game["variant"]),
        join_url=join_url,
        joined=len(game["players"]),
        total=game["total"],
        variant_name=VARIANTS[game["variant"]]["name"],
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
        **_card_context(player["character"], game["variant"]),
        players=_player_list_info(game),
        bandit_teammates=_bandit_teammates(game, token),
        joined=len(game["players"]),
        total=game["total"],
        locked=game["locked"],
        variant_name=VARIANTS[game["variant"]]["name"],
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
