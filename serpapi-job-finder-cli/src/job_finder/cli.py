from __future__ import annotations
import argparse
import json
from job_finder.serpapi_client import SerpApi


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search jobs via SerpApi Google Jobs")
    p.add_argument("--title", required=True, help="Job title keywords")
    p.add_argument("--location", default="United States", help="City/region (default: United States)")
    p.add_argument("--remote", action="store_true", help="Prefer remote roles")
    p.add_argument("--company", default="", help="Filter to a company substring")
    p.add_argument("--limit", type=int, default=20, help="Max results to print")
    p.add_argument("--json-out", help="Optional path to write full JSON results")
    return p.parse_args()


def build_query(args: argparse.Namespace) -> str:
    q = args.title
    if args.company:
        q += f" company:{args.company}"
    if args.remote:
        q += " remote"
    return q


def main() -> None:
    args = parse_args()
    client = SerpApi()
    query = build_query(args)

    data = client.google_jobs(query, hl="en", location=args.location)
    jobs = data.get("jobs_results", [])[: args.limit]

    if not jobs:
        print("No jobs found.")
        return

    for i, j in enumerate(jobs, 1):
        title = j.get("title")
        company = j.get("company_name")
        loc = j.get("location")
        posted = j.get("detected_extensions", {}).get("posted_at", "")
        link = j.get("related_links", [{}])[0].get("link") or j.get("link")
        print(f"{i}. {title} — {company} — {loc} — {posted}")
        if link:
            print(f"   {link}")

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
