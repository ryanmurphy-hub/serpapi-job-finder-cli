# run.py — one-file demo/live runner (stdlib + requests if live)
import os, sys, json, argparse, urllib.parse, urllib.request

API = "https://serpapi.com/search.json"
SAMPLE = {"organic_results": [{"title":"Example","link":"https://example.com"}]*5,
          "jobs_results": [{"title":"Customer Success Engineer","company_name":"Acme","location":"Remote","link":"https://example.com/job"}]*3}

def fetch(engine: str, q: str) -> dict:
    key = os.getenv("SERPAPI_API_KEY")
    if not key:
        raise RuntimeError("Missing SERPAPI_API_KEY (or use --demo)")
    params = {"engine": engine, "q": q, "api_key": key}
    url = API + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--q", default="customer success engineer")
    ap.add_argument("--engine", default="google_jobs")
    ap.add_argument("--limit", type=int, default=5)
    ap.add_argument("--demo", action="store_true")
    args = ap.parse_args()

    data = SAMPLE if args.demo else fetch(args.engine, args.q)
    items = data.get("jobs_results")
    if not isinstance(items, list):
        items = data.get("organic_results")
    if not isinstance(items, list):
        items = []
    items = items[:args.limit]

    for i, it in enumerate(items, 1):
        title = it.get("title") or it.get("job_title") or "N/A"
        link = it.get("link") or ""
        print(f"{i}. {title}\n   {link}")

if __name__ == "__main__":
    main()
