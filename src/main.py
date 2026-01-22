import os
from datetime import datetime

from sources import SOURCES
from fetcher import fetch_rss
from dedup import dedup_items
from llm_deepseek import deepseek_summarize
from feishu import send_feishu_card
from render import render_news_list


def main():
    feishu_webhook = os.getenv("FEISHU_WEBHOOK", "").strip()
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY", "").strip()

    if not feishu_webhook:
        raise RuntimeError("Missing FEISHU_WEBHOOK")
    if not deepseek_api_key:
        raise RuntimeError("Missing DEEPSEEK_API_KEY")

    all_items = []
    for s in SOURCES:
        if s["type"] == "rss":
            all_items.extend(fetch_rss(
                url=s["url"],
                source_name=s["name"],
                category=s["category"],
                hours=48
            ))

    all_items = dedup_items(all_items)

    # 简单排序：有发布时间的优先
    all_items.sort(key=lambda x: x.get("published", ""), reverse=True)

    analysis = deepseek_summarize(deepseek_api_key, all_items, max_items=12)
    news_list_md = render_news_list(all_items, limit=12)

    today = datetime.now().strftime("%Y-%m-%d")
    title = f"汽车行业快报 | {today}"

    md = f"""
**过去48小时重点新闻（Top 12）**
{news_list_md}

---

**DeepSeek 解读**
{analysis}
""".strip()

    send_feishu_card(
        webhook_url=feishu_webhook,
        title=title,
        markdown_text=md
    )


if __name__ == "__main__":
    main()
