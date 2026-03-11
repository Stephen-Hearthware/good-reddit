import json
import time
import feedparser

SUBREDDITS = [
    "askphilosophy",
    "AskHistorians",
    "askscience",
    "meditation",
    "AnimalBehavior",
    "woodworking",
    "upliftingnews",
]

def fetch(sub):
    url = f"https://www.reddit.com/r/{sub}/top/.rss?t=day"

    feed = feedparser.parse(url)

    posts = []

    for entry in feed.entries[:15]:
        posts.append({
            "id": entry.id,
            "title": entry.title,
            "subreddit": sub,
            "author": entry.author,
            "score": 0,
            "comments": 0,
            "preview": entry.summary[:200] if hasattr(entry, "summary") else "",
            "url": entry.link,
            "commentsUrl": entry.link,
            "domain": "reddit",
            "category": "General"
        })

    return posts


posts = []

for sub in SUBREDDITS:
    print(f"Fetching r/{sub}")

    try:
        posts.extend(fetch(sub))
    except Exception as e:
        print(f"Skipping r/{sub}: {e}")

    time.sleep(1)


print(f"Collected {len(posts)} posts")

with open("docs/feed.json", "w") as f:
    json.dump(
        {
            "generated": int(time.time()),
            "posts": posts
        },
        f,
        indent=2
    )

print("feed.json written")