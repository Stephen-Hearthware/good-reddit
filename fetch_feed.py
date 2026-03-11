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

USER_AGENT = "good-reddit-reader/0.1"


def fetch(sub):
    url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit=15"
    r = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()["data"]["children"]


posts = []

for sub in SUBREDDITS:
    data = fetch(sub)

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

    time.sleep(1)

with open("feed.json", "w") as f:
    json.dump(
        {
            "generated": int(time.time()),
            "posts": posts,
        },
        f,
        indent=2,
    )