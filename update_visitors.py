import os
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone

GITHUB_TOKEN = os.environ.get("TRAFFIC_TOKEN") or os.environ.get("GITHUB_TOKEN")
REPO = "Wegnernando94/wegnernando94"
STATS_FILE = "visitor-stats.json"
README_FILE = "README.md"


def fetch_traffic():
    url = f"https://api.github.com/repos/{REPO}/traffic/views"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "github-actions-visitor-counter",
    })
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read())


def load_stats():
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"total": 0, "today": 0, "last_updated": "", "history": []}


def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)


def update_readme(today_count, total_count):
    with open(README_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    badge_url = (
        f"https://img.shields.io/badge/👁️_Visitas_Hoje-{today_count}"
        f"-00b4d8?style=for-the-badge&labelColor=0d1117"
    )
    total_badge_url = (
        f"https://img.shields.io/badge/📊_Total_de_Visitas-{total_count}"
        f"-0077b6?style=for-the-badge&labelColor=0d1117"
    )

    new_block = (
        f'  <!-- VISITOR_BADGES_START -->\n'
        f'  <img src="{badge_url}" alt="Visitas hoje"/>\n'
        f'  <img src="{total_badge_url}" alt="Total de visitas"/>\n'
        f'  <!-- VISITOR_BADGES_END -->'
    )

    if "<!-- VISITOR_BADGES_START -->" in content:
        content = re.sub(
            r'  <!-- VISITOR_BADGES_START -->.*?<!-- VISITOR_BADGES_END -->',
            new_block,
            content,
            flags=re.DOTALL,
        )
    else:
        content = content.replace(
            '<img src="https://komarev.com/ghpvc/',
            f'{new_block}\n  <img src="https://komarev.com/ghpvc/',
        )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    stats = load_stats()

    try:
        traffic = fetch_traffic()
    except urllib.error.HTTPError as e:
        print(f"Erro ao buscar traffic: {e}")
        return

    api_total = traffic.get("count", 0)
    today_count = 0
    for view in traffic.get("views", []):
        if view["timestamp"].startswith(today_str):
            today_count = view["count"]
            break

    # Atualiza histórico
    history = {entry["date"]: entry for entry in stats.get("history", [])}
    history[today_str] = {"date": today_str, "count": today_count}
    stats["history"] = sorted(history.values(), key=lambda x: x["date"])[-30:]
    stats["today"] = today_count
    stats["total"] = api_total
    stats["last_updated"] = datetime.now(timezone.utc).isoformat()

    save_stats(stats)
    update_readme(today_count, api_total)

    print(f"✅ {today_str} | Hoje: {today_count} | Total: {api_total}")


if __name__ == "__main__":
    main()
