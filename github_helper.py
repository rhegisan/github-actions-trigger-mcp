# github_helper.py
import os
import requests
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_OWNER = os.environ.get("GITHUB_OWNER")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

if not (GITHUB_TOKEN and GITHUB_OWNER and GITHUB_REPO):
    # Keep this lazy so importing for lint/tests fails fast
    raise RuntimeError("GITHUB_TOKEN, GITHUB_OWNER and GITHUB_REPO must be set as env vars")

API_BASE = "https://api.github.com"
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

def trigger_workflow_dispatch(workflow_filename: str, ref: str = "master", inputs: Optional[Dict[str, Any]] = None) -> None:
    """
    Trigger a workflow_dispatch on GitHub.
    Raises RuntimeError on failure (caller can map to MCPError).
    """
    url = f"{API_BASE}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/actions/workflows/{workflow_filename}/dispatches"
    body = {"ref": ref}
    if inputs:
        body["inputs"] = inputs

    resp = requests.post(url, json=body, headers=HEADERS)
    # Successful dispatch returns HTTP 204 No Content
    if resp.status_code == 204:
        return
    # GitHub often returns JSON error. Raise with details.
    try:
        payload = resp.json()
    except Exception:
        payload = resp.text
    raise RuntimeError(f"GitHub API returned {resp.status_code}: {payload}")
