import feedparser
from dateutil import parser as dtparser
from datetime import datetime, timezone, timedelta


def fetch_rss(url: str, source_name: str, category: str, hours: int = 48):
    feed = feedparser.parse(url)
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=hours)

    items = []
    for entry in feed.entries:
        published = None

        if hasattr(entry, "published"):
            try:
                published = dtparser.parse(entry.published)
                if published.tzinfo is None:
                    published = published.replace(tzinfo=timezone.utc)
            except Exception:
                published = None

        # 有些 RSS 没 published，直接收录但降低权重
        if published and published < cutoff:
            continue

        items.append({
            "source": source_name,
            "category": category,
            "title": entry.get("title", "").strip(),
            "link": entry.get("link", "").strip(),
            "published": published.isoformat() if published else "",
            "summary": (entry.get("summary", "") or "").strip()
        })

    return items
