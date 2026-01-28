# tools/web_tools.py

import requests


def web_search(query: str):
    """
    Simple web search using DuckDuckGo (basic fallback).
    Returns raw text snippet.
    """

    try:
        url = f"https://duckduckgo.com/?q={query}&format=json"

        headers = {
            "User-Agent": "Jarvis-Agent/1.0"
        }

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code != 200:
            return f"Search failed: HTTP {r.status_code}"

        return r.text[:4000]   # limit output


    except Exception as e:

        return f"Search error: {e}"
