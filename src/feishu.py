import requests


def send_feishu_card(webhook_url: str, title: str, markdown_text: str):
    card = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {
                "title": {"tag": "plain_text", "content": title}
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": markdown_text}
                }
            ]
        }
    }

    resp = requests.post(webhook_url, json=card, timeout=30)
    resp.raise_for_status()
    return resp.json()
