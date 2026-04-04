# MTG Commander Kingdom

A self-hosted web app for playing **Advanced Kingdoms**, the hidden-role EDH variant.

Players join via a shared link and each see only their own secret role. Once all players have joined the game is locked.

---

## Roles & win conditions

| Role | Team | Win condition |
|------|------|---------------|
| 👑 King | Royal | Only you and Knights remain. Starts at **50 life**, role is **public**. |
| ⚔️ Knight | Royal | King survives and all Assassins/Bandits/Renegades are eliminated. |
| 🗡️ Assassin | Assassins | Last player standing — but Bandits must die before the King does. |
| 💀 Bandit | Bandits | At least one Bandit is alive when the King is eliminated. |
| 🌀 Renegade | None | Last player standing. |

**Role distribution by player count**

| Players | Roles |
|---------|-------|
| 3 | King · Assassin · Bandit |
| 4 | + Knight |
| 5 | + Renegade |
| 6 | + 2nd Knight |
| 7 | + 2nd Assassin |
| 8 | + 2nd Bandit |
| 9 | + 3rd Knight |
| 10 | + 2nd Renegade |

---

## Hosting on TrueNAS SCALE

> Tested on TrueNAS SCALE 24.10 (Electric Eel) and later. Requires the **Apps** service to be enabled or Docker available via SSH.

### Option A — SSH + Docker Compose (recommended)

1. **Open a shell** on your TrueNAS box (Web UI → System → Shell, or SSH).

2. **Pick a dataset** to store the app, e.g. `/mnt/tank/apps/mtg-kingdom`:
   ```bash
   mkdir -p /mnt/tank/apps/mtg-kingdom
   cd /mnt/tank/apps/mtg-kingdom
   ```

3. **Clone this repo**:
   ```bash
   git clone https://github.com/tobiwan88/mtg_kimgdom.git .
   ```

4. **Start the container**:
   ```bash
   docker compose up -d
   ```
   The app is now running on port **5000**.

5. **Check it's up**:
   ```bash
   docker compose ps
   # open http://<truenas-ip>:5000 in your browser
   ```

6. **Use a different port** (optional):
   ```bash
   PORT=8080 docker compose up -d
   ```

7. **Update to a new version**:
   ```bash
   git pull
   docker compose up -d --build
   ```

8. **Stop / remove**:
   ```bash
   docker compose down
   ```

---

### Option B — TrueNAS Custom App (GUI, no SSH needed)

> Available in TrueNAS SCALE Electric Eel (24.10+) via **Apps → Discover → Custom App**.

1. Go to **Apps → Discover Apps → Custom App**.
2. Choose **Docker Compose** as the deployment type.
3. Paste the following into the compose editor and click **Save**:

```yaml
services:
  mtg-kingdom:
    image: ghcr.io/tobiwan88/mtg_kimgdom:latest
    restart: unless-stopped
    ports:
      - "5000:5000"
```

> If you haven't published a pre-built image, use Option A (build from source) instead.

---

## Quick start (non-TrueNAS / any Linux)

```bash
git clone https://github.com/tobiwan88/mtg_kimgdom.git
cd mtg_kimgdom
docker compose up -d
# open http://localhost:5000
```

Or without Docker:
```bash
pip install flask
python app.py
```

---

## Configuration

| Environment variable | Default | Description |
|----------------------|---------|-------------|
| `PORT` | `5000` | Port the app listens on |

---

## Notes

- **Game state is in-memory.** Restarting the container clears all active games.
- The app is designed for **local network play**. If you expose it to the internet, put it behind a reverse proxy (e.g. Nginx Proxy Manager, which is available as a TrueNAS app).
- Player count: **3–12 players**.
