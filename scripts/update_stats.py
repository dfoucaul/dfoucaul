"""Render public GitHub statistics with the Python standard library only."""

from datetime import datetime, timedelta, timezone
from html import escape
import json
import os
from pathlib import Path
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
USERNAME = os.environ.get("PROFILE_USERNAME", "dfoucaul")
if not re.fullmatch(r"[A-Za-z0-9-]+", USERNAME):
    raise ValueError("Invalid GitHub username")


def github(path):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-public-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/{path}", headers=headers)
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            if error.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except URLError:
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)


def search_count(resource, query):
    data = github(f"search/{resource}?{urlencode({'q': query, 'per_page': 1})}")
    if data.get("incomplete_results"):
        raise RuntimeError("GitHub returned incomplete statistics; keeping the previous card")
    return data["total_count"]


def main():
    today = datetime.now(timezone.utc).date()
    since = today - timedelta(days=364)
    repos = []
    page = 1
    while True:
        batch = github(f"users/{USERNAME}/repos?type=owner&per_page=100&page={page}")
        repos.extend(
            repo for repo in batch
            if not repo["private"] and not repo["fork"]
            and repo["name"].lower() != USERNAME.lower()
        )
        if len(batch) < 100:
            break
        page += 1

    commits = search_count(
        "commits", f"author:{USERNAME} author-date:{since}..{today} is:public"
    )
    prs = search_count("issues", f"author:{USERNAME} type:pr is:public")
    stars = sum(repo["stargazers_count"] for repo in repos)
    metrics = [
        (len(repos), "PROJETS PUBLICS", "Hors forks et dépôt de profil"),
        (commits, "COMMITS / 365 JOURS", "Commits publics indexés par GitHub"),
        (prs, "PULL REQUESTS", "Contributions publiques, toutes périodes"),
        (stars, "ÉTOILES REÇUES", "Sur mes projets publics"),
    ]
    blocks = []
    for index, (value, label, note) in enumerate(metrics):
        x = 36 + (index % 2) * 420
        y = 100 + (index // 2) * 160
        blocks.append(f'''<g transform="translate({x},{y})">
          <text y="0" fill="#c7fa73" font-size="64" font-weight="700">{value:02d}</text>
          <text y="36" fill="#f3f3e6" font-size="22" letter-spacing="1">{escape(label)}</text>
          <text y="62" fill="#a7b0a5" font-size="15">{escape(note)}</text>
        </g>''')
    description = "; ".join(f"{value} {label}" for value, label, _ in metrics)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="400" viewBox="0 0 900 400" role="img" aria-labelledby="title desc">
      <title id="title">Statistiques publiques de {escape(USERNAME)}</title>
      <desc id="desc">{escape(description)}. Mise à jour : {today} UTC.</desc>
      <rect width="900" height="400" rx="2" fill="#101512"/>
      <rect x="1" y="1" width="898" height="398" rx="2" fill="none" stroke="#354137"/>
      <g font-family="'DejaVu Sans Mono', Consolas, monospace">
        <text x="36" y="32" fill="#a7b0a5" font-size="14" letter-spacing="2">PUBLIC SIGNAL / GITHUB</text>
        <path d="M450 62v276 M36 205h828" stroke="#354137"/>
        {''.join(blocks)}
        <rect x="36" y="369" width="8" height="8" fill="#c7fa73"/>
        <text x="56" y="378" fill="#a7b0a5" font-size="14">MISE À JOUR / {today} UTC</text>
      </g>
    </svg>
    '''
    destination = ROOT / "assets" / "statistics.svg"
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".svg.tmp")
    temporary.write_text(svg.strip() + "\n", encoding="utf-8")
    temporary.replace(destination)
    print(description)


if __name__ == "__main__":
    main()
