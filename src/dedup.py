import hashlib


def _hash_key(title: str, link: str) -> str:
    raw = (title.strip().lower() + "|" + link.strip().lower()).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def dedup_items(items):
    seen = set()
    out = []
    for it in items:
        key = _hash_key(it.get("title", ""), it.get("link", ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(it)
    return out
