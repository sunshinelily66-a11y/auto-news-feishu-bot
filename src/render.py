def render_news_list(items, limit=12):
    lines = []
    for it in items[:limit]:
        lines.append(f"- [{it['title']}]({it['link']})  ({it['source']} | {it['category']})")
    return "\n".join(lines)
