"""
Reddit search scraper for /reddit slash command.

Hits old.reddit.com /.json endpoints with a proper UA. No auth required.
Pulls posts across multiple sort orders to maximize recency coverage (Reddit
search caps results at ~250 per sort; mixing sorts widens the time window).

Usage:
  python reddit_search.py --topic "fleet maintenance" --limit 200 --output out.json
  python reddit_search.py --topic "ServiceTitan complaints" --subreddit HVAC --limit 100 --output out.json

Output JSON shape:
  {
    "topic": "...",
    "subreddit": "HVAC" | null,
    "collected_at_utc": 1234567890,
    "posts": [ {id, subreddit, title, selftext, author, created_utc, score, num_comments, permalink, top_comments: [...]}, ... ]
  }
"""
import argparse
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

UA = "PersonalBrain-Reddit-Skill/1.0"
PER_PAGE = 25
MAX_PAGES = 10
INTER_REQ_SLEEP = 1.2


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def search_one_sort(topic, subreddit, sort, time_window, limit):
    posts = []
    after = None
    pages = 0
    while len(posts) < limit and pages < MAX_PAGES:
        params = {"q": topic, "sort": sort, "limit": PER_PAGE, "t": time_window}
        if subreddit:
            params["restrict_sr"] = "on"
            base = f"https://www.reddit.com/r/{subreddit}/search.json"
        else:
            base = "https://www.reddit.com/search.json"
        if after:
            params["after"] = after
        url = f"{base}?{urllib.parse.urlencode(params)}"
        try:
            data = fetch_json(url)
        except Exception as e:
            print(f"  error ({sort}): {e}", file=sys.stderr)
            break
        children = data.get("data", {}).get("children", [])
        if not children:
            break
        for c in children:
            p = c["data"]
            posts.append({
                "id": p.get("id"),
                "subreddit": p.get("subreddit"),
                "title": p.get("title"),
                "selftext": p.get("selftext", ""),
                "author": p.get("author"),
                "created_utc": p.get("created_utc"),
                "score": p.get("score"),
                "num_comments": p.get("num_comments"),
                "permalink": f"https://reddit.com{p.get('permalink','')}",
            })
        after = data.get("data", {}).get("after")
        if not after:
            break
        pages += 1
        time.sleep(INTER_REQ_SLEEP)
    return posts[:limit]


def search(topic, subreddit, limit):
    """Search across multiple sort orders and dedupe by post id to widen time coverage."""
    per_sort = max(50, limit // 3)
    all_posts = {}
    for sort, tw in [("relevance", "all"), ("new", "all"), ("top", "all")]:
        batch = search_one_sort(topic, subreddit, sort, tw, per_sort)
        for p in batch:
            if p["id"] and p["id"] not in all_posts:
                all_posts[p["id"]] = p
        time.sleep(INTER_REQ_SLEEP)
    return list(all_posts.values())


def fetch_top_comments(permalink, limit=10):
    """Fetch top N comments for a post, ranked by score."""
    url = permalink.rstrip("/") + ".json?limit=50&sort=top"
    try:
        data = fetch_json(url)
    except Exception:
        return []
    if not isinstance(data, list) or len(data) < 2:
        return []
    out = []

    def walk(children):
        for c in children:
            if c.get("kind") != "t1":
                continue
            d = c.get("data", {})
            body = d.get("body", "")
            if body and body not in ("[deleted]", "[removed]"):
                out.append({
                    "author": d.get("author"),
                    "score": d.get("score"),
                    "body": body,
                    "created_utc": d.get("created_utc"),
                })
            replies = d.get("replies")
            if isinstance(replies, dict):
                walk(replies.get("data", {}).get("children", []))

    walk(data[1].get("data", {}).get("children", []))
    out.sort(key=lambda c: c.get("score") or 0, reverse=True)
    return out[:limit]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", required=True, help="search query / topic")
    ap.add_argument("--subreddit", default=None, help="optional subreddit restriction")
    ap.add_argument("--limit", type=int, default=200, help="max unique posts to collect")
    ap.add_argument("--output", required=True, help="path to write JSON output")
    ap.add_argument("--top-comments", type=int, default=10,
                    help="fetch top N comments for the top K posts (K=20). 0 to skip.")
    args = ap.parse_args()

    print(f"[reddit] searching '{args.topic}'"
          + (f" in r/{args.subreddit}" if args.subreddit else ""), file=sys.stderr)
    posts = search(args.topic, args.subreddit, args.limit)
    print(f"[reddit] got {len(posts)} unique posts across sorts", file=sys.stderr)

    if args.top_comments > 0 and posts:
        ranked = sorted(posts,
                        key=lambda p: (p.get("score") or 0) + 2 * (p.get("num_comments") or 0),
                        reverse=True)
        top_k = ranked[:20]
        top_ids = {p["id"] for p in top_k}
        print(f"[reddit] fetching comments for top {len(top_k)} posts", file=sys.stderr)
        for p in posts:
            if p["id"] in top_ids:
                p["top_comments"] = fetch_top_comments(p["permalink"], args.top_comments)
                time.sleep(INTER_REQ_SLEEP)
            else:
                p["top_comments"] = []

    out = {
        "topic": args.topic,
        "subreddit": args.subreddit,
        "collected_at_utc": int(time.time()),
        "posts": posts,
    }
    pathlib.Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(args.output).write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(f"[reddit] wrote {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
