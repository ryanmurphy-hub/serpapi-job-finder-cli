from __future__ import annotations
from unittest.mock import patch
from job_finder.serpapi_client import SerpApi


@patch("job_finder.serpapi_client.requests.get")
def test_google_jobs_mocked(req):
    req.return_value.status_code = 200
    req.return_value.json.return_value = {
        "jobs_results": [{"title": "CSE", "company_name": "SerpApi", "location": "Remote"}]
    }
    s = SerpApi(api_key="fake")
    out = s.google_jobs("customer success engineer", location="United States")
    assert "jobs_results" in out
    assert out["jobs_results"][0]["company_name"] == "SerpApi"
