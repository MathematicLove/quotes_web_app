import random
import requests

from django.core.cache import cache

WIKI_THUMB_CACHE_1H = 60 * 60

def weighted_choice(quotes):
    population = [q for q, _ in quotes]
    weights = [w for _, w in quotes]
    return random.choices(population=population, weights=weights, k=1)[0]

def wikipedia_thumb_for_title(title: str, size: int = 400) -> str | None:
    cache_key = f"wiki_thumb:{size}:{title}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    api = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "pageimages",
        "format": "json",
        "pithumbsize": size,
        "titles": title
    }
    try:
        r = requests.get(api, params=params, timeout=6)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            thumb = page.get("thumbnail", {})
            src = thumb.get("source")
            if src:
                cache.set(cache_key, src, WIKI_THUMB_CACHE_1H)
                return src
    except Exception:
        pass
    cache.set(cache_key, None, 300)
    return None
