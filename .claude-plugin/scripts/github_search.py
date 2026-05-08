"""
GitHub search scraper for /github slash command.

Searches public repos matching a problem/topic. For the top 100 returned,
collects metadata (stars, last-commit, language, description). For the top
candidates by relevance+activity, fetches README text + top issues.

Usage:
  python github_search.py --topic "llm eval harness" --output out.json
  python github_search.py --topic "python retry decorator" --deep 5 --output out.json

Auth: uses GITHUB_TOKEN env var if set (5000 req/hr authenticated vs 60 unauthenticated).
Without a token, script throttles to stay under 60/hr and limits --deep to 5.

Output JSON shape:
  {
    "topic": "...",
    "collected_at_utc": 1234567890,
    "authenticated": true|false,
    "repos": [
      {
        "full_name": "org/repo",
        "description": "...",
        "stars": N,
        "forks": N,
        "language": "Python",
        "created_at": "...",
        "pushed_at": "...",  # last commit
        "archived": bool,
        "topics": [...],
        "html_url": "...",
        "readme": "..." | null,     # populated for deep-dive repos
        "issues": [ {title, body, comments, state, created_at, html_url}, ... ] | null
      }, ...
    ]
  }
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.parse
import urllib.request

UA = "PersonalBrain-GitHub-Skill/1.0"
API = "https://api.github.com"


def _headers(token):
    h = {
        "User-Agent": UA,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fetch(url, token, accept=None):
    req = urllib.request.Request(url, headers=_headers(token))
    if accept:
        req.add_header("Accept", accept)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def fetch_json(url, token):
    return json.loads(fetch(url, token))


def search_repos(topic, token, min_count=100):
    """Search repos, paginating up to min_count results. Max is 1000 per GitHub API."""
    repos = []
    per_page = 100
    page = 1
    sleep = 0.5 if token else 1.5
    while len(repos) < min_count and page <= 10:
        params = {
            "q": topic,
            "sort": "stars",
            "order": "desc",
            "per_page": per_page,
            "page": page,
        }
        url = f"{API}/search/repositories?{urllib.parse.urlencode(params)}"
        try:
            data = fetch_json(url, token)
        except Exception as e:
            print(f"  search error page {page}: {e}", file=sys.stderr)
            break
        items = data.get("items", [])
        if not items:
            break
        for it in items:
            repos.append({
                "full_name": it.get("full_name"),
                "description": it.get("description"),
                "stars": it.get("stargazers_count"),
                "forks": it.get("forks_count"),
                "language": it.get("language"),
                "created_at": it.get("created_at"),
                "pushed_at": it.get("pushed_at"),
                "archived": it.get("archived"),
                "topics": it.get("topics", []),
                "html_url": it.get("html_url"),
                "readme": None,
                "issues": None,
            })
        page += 1
        time.sleep(sleep)
    return repos


def fetch_readme(full_name, token):
    url = f"{API}/repos/{full_name}/readme"
    try:
        raw = fetch(url, token, accept="application/vnd.github.raw")
        text = raw.decode("utf-8", errors="replace")
        if len(text) > 20000:
            text = text[:20000] + "\n\n[TRUNCATED]"
        return text
    except Exception as e:
        print(f"  readme error {full_name}: {e}", file=sys.stderr)
        return None


def fetch_top_issues(full_name, token, limit=15):
    """Fetch issues sorted by comment count (proxy for most-discussed pain/asks)."""
    params = {"state": "all", "sort": "comments", "direction": "desc", "per_page": limit}
    url = f"{API}/repos/{full_name}/issues?{urllib.parse.urlencode(params)}"
    try:
        data = fetch_json(url, token)
    except Exception as e:
        print(f"  issues error {full_name}: {e}", file=sys.stderr)
        return []
    issues = []
    for it in data:
        if it.get("pull_request"):
            continue
        body = it.get("body") or ""
        if len(body) > 3000:
            body = body[:3000] + "\n[TRUNCATED]"
        issues.append({
            "number": it.get("number"),
            "title": it.get("title"),
            "body": body,
            "comments": it.get("comments"),
            "state": it.get("state"),
            "created_at": it.get("created_at"),
            "html_url": it.get("html_url"),
        })
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, help="search query / problem description")
    ap.add_argument("--min-repos", type=int, default=100,
                    help="minimum number of repos to surface (metadata only)")
    ap.add_argument("--deep", type=int, default=10,
                    help="for this many top repos, also fetch README + issues")
    ap.add_argument("--output", required=True, help="path to write JSON output")
    args = ap.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("[github] no GITHUB_TOKEN in env — using unauthenticated mode (60 req/hr)",
              file=sys.stderr)
        if args.deep > 5:
            print(f"[github] capping --deep from {args.deep} to 5 (unauth rate limit)",
                  file=sys.stderr)
            args.deep = 5

    print(f"[github] searching '{args.topic}' (min {args.min_repos} repos)", file=sys.stderr)
    repos = search_repos(args.topic, token, args.min_repos)
    print(f"[github] got {len(repos)} repos", file=sys.stderr)

    deep_targets = repos[:args.deep]
    for i, r in enumerate(deep_targets):
        print(f"[github] deep-dive {i+1}/{len(deep_targets)}: {r['full_name']}",
              file=sys.stderr)
        r["readme"] = fetch_readme(r["full_name"], token)
        time.sleep(0.5 if token else 1.2)
        r["issues"] = fetch_top_issues(r["full_name"], token)
        time.sleep(0.5 if token else 1.2)

    out = {
        "topic": args.topic,
        "collected_at_utc": int(time.time()),
        "authenticated": bool(token),
        "repos": repos,
    }
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.output).write_text(json.dumps(out, indent=2, default=str),
                                         encoding="utf-8")
    print(f"[github] wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
