import json
import time

import requests

SUBREDDITS = [
    "askphilosophy",
    "AskHistorians",
    "askscience",
    "meditation",
    "AnimalBehavior",
    "woodworking",
    "upliftingnews",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; GoodRedditReader/0.1; +https://github.com/Stephen-Hearthware/good-reddit)",
    "Accept": "application/json",
}

def fetch(sub):
    url = f"https://old.reddit.com/r/{sub}/top.json?t=day&limit=15"

    r = requests.get(
        url,
        headers=HEADERS,
        timeout=20,
    )

    r.raise_for_status()

    return r.json()["data"]["children"]


posts = []

for sub in SUBREDDITS:
    print(f"Fetching r/{sub}")

    try:
        data = fetch(sub)
    except Exception as e:
        print(f"Skipping r/{sub}: {e}")
        continue

    for item in data:
        p = item["data"]

        preview = (p.get("selftext") or "")[:200]

        posts.append(
            {
                "id": p["id"],
                "title": p["title"],
                "subreddit": p["subreddit"],
                "author": p["author"],
                "score": p["score"],
                "comments": p["num_comments"],
                "preview": preview,
                "url": "https://reddit.com" + p["permalink"],
                "commentsUrl": "https://reddit.com" + p["permalink"],
                "domain": p["domain"],
                "category": "General",
            }
        )

    time.sleep(2)


print(f"Collected {len(posts)} posts")

with open("feed.json", "w") as f:
    json.dump(
        {
            "generated": int(time.time()),
            "posts": posts,
        },
        f,
        indent=2,
    )

print("feed.json written")