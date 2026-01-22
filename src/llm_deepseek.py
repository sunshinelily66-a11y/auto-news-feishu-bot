import requests


def deepseek_summarize(api_key: str, items: list, max_items: int = 12) -> str:
    items = items[:max_items]

    bullets = []
    for i, it in enumerate(items, 1):
        bullets.append(
            f"{i}. [{it['category']}] {it['title']}\n"
            f"来源: {it['source']}\n"
            f"链接: {it['link']}\n"
            f"摘要: {it['summary'][:400]}"
        )

    user_content = "\n\n".join(bullets)

    prompt = f"""
你是一位汽车行业分析师。请基于以下新闻，输出一份“中文行业快报”，要求：

1）先给一句话总览（<=30字）
2）按主题分组：车企动态 / 智能驾驶 / 供应链与制造 / 政策与监管 / 投融资与商业化（没有就略过）
3）每组给出要点（每条<=40字）
4）给出“影响判断”：对行业格局、价格战、技术路线、供应链风险的影响
5）给出“接下来48小时值得盯的信号”（3条）
6）语言务实、偏商业解读，避免空话

新闻如下：
{user_content}
""".strip()

    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    return data["choices"][0]["message"]["content"].strip()
