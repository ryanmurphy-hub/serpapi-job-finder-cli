import argparse
import os
import json
import time
import requests
from dotenv import load_dotenv

# Small built-in sample so you can demo without a key or internet
SAMPLE = {
    "jobs_results": [
        {
            "title": "Customer Success Engineer",
            "company_name": "Acme Corp",
            "location": "Remote",
            "link": "https://example.com/job-1",
        },
        {
            "title": "Solutions Consultant",
            "company_name": "Beta Inc",
            "location": "Austin, TX",
            "link": "https://example.com/job-2",
        },
        {
            "title": "Sales Engineer (API)",
            "company_name": "Gamma",
            "location": "Denver, CO",
            "link": "https://example.com/job-3",
        },
    ]
}


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the SerpApi Job Finder CLI."""
    p = argparse.ArgumentParser(description="Search jobs via SerpApi Google Jobs")
    p.add_argument("--title", default="customer success engineer",
                   help="Job title keywords (default: customer success engineer)")
    p.add_argument("--location", default="United States",
                   help="City/region (default: United States)")
    p.add_argument("--remote", action="store_true",
                   help="Prefer remote roles")
    p.add_argument("--company", default="",
                   help="Filter to a company substring")
    p.add_argument("--limit", type=int, default=20,
                   help="Max results to print")
    p.add_argument("--json-out",
                   help="Optional path to write JSON results")
    p.add_argument("--demo", action="store_true",
                   help="Run with bundled sample data (no key or internet required)")
    return p.parse_args()


def search_jobs(
    title: str,
    location: str,
    remote: bool,
    company: str,
    limit: int,
) -> list[dict]:
    """Perform a job search via SerpApi."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing SERPAPI_API_KEY in environment or .env file")

    params = {
        "engine": "google_jobs",
        "q": title,
        "location": location,
        "api_key": api_key,
    }
    if remote:
        params["remote"] = "true"

    # Gentle retry on 429; fail fast on other errors
    url = "https://serpapi.com/search.json"
    for i in range(3):
        resp = requests.get(url, params=params, timeout=30)
        if resp.status_code == 200:
            break
        if resp.status_code == 429:
            time.sleep(2 ** i)
            continue
        resp.raise_for_status()
    results = resp.json()

    jobs = results.get("jobs_results", [])
    if not isinstance(jobs, list):
        jobs = []
    if company:
        needle = company.lower()
        jobs = [
            j for j in jobs
            if needle in ((j.get("company_name") or j.get("company") or "").lower())
        ]
    return jobs[:limit]


def print_jobs(jobs: list[dict]) -> None:
    for i, job in enumerate(jobs, 1):
        title = job.get("title") or job.get("job_title") or "N/A"
        company = job.get("company_name") or job.get("company") or "N/A"
        location = job.get("location", "N/A")
        link = job.get("link", "N/A")
        print(f"{i}. {title} — {company} — {location}")


def main() -> None:
    """Main entrypoint for the CLI."""
    load_dotenv()
    args = parse_args()

    if args.demo:
        jobs = SAMPLE["jobs_results"][: args.limit]
        if args.company:
            needle = args.company.lower()
            jobs = [
                j for j in jobs
                if needle in ((j.get("company_name") or j.get("company") or "").lower())
            ]
    else:
        jobs = search_jobs(
            args.title,
            args.location,
            args.remote,
            args.company,
            args.limit,
        )

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {args.json_out}")
    else:
        print_jobs(jobs)


if __name__ == "__main__":
    main()
