import argparse
import os
import requests
from dotenv import load_dotenv


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the SerpApi Job Finder CLI."""
    parser = argparse.ArgumentParser(
        description="Search jobs via SerpApi Google Jobs"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="Job title keywords",
    )
    parser.add_argument(
        "--location",
        default="United States",
        help="City/region (default: United States)",
    )
    parser.add_argument(
        "--remote",
        action="store_true",
        help="Prefer remote roles",
    )
    parser.add_argument(
        "--company",
        default="",
        help="Filter to a company substring",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Max results to print",
    )
    parser.add_argument(
        "--json-out",
        help="Optional path to write full JSON results",
    )
    return parser.parse_args()


def search_jobs(
    title: str,
    location: str,
    remote: bool,
    company: str,
    limit: int,
) -> dict:
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

    response = requests.get("https://serpapi.com/search", params=params, timeout=30)
    response.raise_for_status()
    results = response.json()

    jobs = results.get("jobs_results", [])[:limit]

    if company:
        jobs = [
            job
            for job in jobs
            if company.lower() in job.get("company_name", "").lower()
        ]

    return jobs


def main() -> None:
    """Main entrypoint for the CLI."""
    load_dotenv()
    args = parse_args()

    jobs = search_jobs(
        args.title,
        args.location,
        args.remote,
        args.company,
        args.limit,
    )

    if args.json_out:
        import json

        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(jobs)} jobs to {args.json_out}")
    else:
        for i, job in enumerate(jobs, 1):
            title = job.get("title", "N/A")
            company = job.get("company_name", "N/A")
            location = job.get("location", "N/A")
            link = job.get("link", "N/A")

            print(f"{i}. {title} — {company} — {location}")
            print(f"   {link}")


if __name__ == "__main__":
    main()
