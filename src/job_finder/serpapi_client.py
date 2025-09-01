from __future__ import annotations
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://serpapi.com/search.json"


class SerpApi:
    """Minimal SerpApi client for Google Jobs."""

    def __init__(self, api_key: str | None = None) -> None:
        self.key = api_key or os.getenv("SERPAPI_API_KEY")
        if not self.key:
            raise ValueError("SERPAPI_API_KEY is not set")

    def google_jobs(self, q: str, **params) -> dict:
        payload = {"engine": "google_jobs", "q": q, "api_key": self.key, **params}
        r = requests.get(BASE_URL, params=payload, timeout=30)
        r.raise_for_status()
        return r.json()
