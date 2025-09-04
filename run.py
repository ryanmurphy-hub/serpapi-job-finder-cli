# run.py (stdlib only)
import os, sys, json, argparse, urllib.parse, urllib.request

API = "https://serpapi.com/search.json"

SAMPLE = {
    "organic_results": [
        {"title": "What is a Customer Success Engineer?", "link": "https://example.com/cse"},
        {"title": "API troubleshooting basics", "link": "https://example.com/api"},
        {"title": "Pagination and rate limits", "link": "https://example.com/pagination"},
        {"title": "JSON parsing with Python", "link": "https://example.com/json"},
        {"title": "Interview prep checklist", "link": "https://example.com/prep"}
    ],
    "jobs_results": [
        {"job_title": "Customer Success Engineer", "link": "https://example.com/job-1"},
        {"job_title": "Solutions Consultant", "link": "https://example.com/job-2"},
        {"job_title": "Sales Engineer (API)", "link": "https://example.com/job-3"},
    ]
}

def fetch(engine: str, q: str) -> dict:
    key = os.getenv("SERPAPI_API_KEY")
    if not key:
        raise RuntimeError("Missing SERPAPI_API_KEY (or run with --demo)")
    params = {"engine": engine, "q": q, "api_key": key}
    url = API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    ap = argparse.ArgumentParser(description="Tiny SerpApi runner")
    ap.add_argument("--q", default="customer success engineer")
    ap.add_argument("--engine", default="google")  # or "google_jobs"
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--demo", action="store_true", help="Run without API key or internet using sample data")
    args = ap.parse_args()

    try:
        data = SAMPLE if args.demo else fetch(args.engine, args.q)
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        print("Tip: run with --demo to show output without a key/network.", file=sys.stderr)
        sys.exit(1)

    items = (data.get("jobs_results") or data.get("organic_results") or [])[:args.limit]
    for i, it in enumerate(items, 1):
        title = it.get("title") or it.get("job_title") or "N/A"
        link = it.get("link") or ""
        print(f"{i}. {title}\n   {link}")

if __name__ == "__main__":
    main()
