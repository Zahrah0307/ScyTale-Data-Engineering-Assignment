"""extract.py - Fetch merged PRs and save to data/raw"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import argparse
from github_api import fetch_closed_prs

logging.basicConfig(level=logging.INFO, format="%(message)s")

def get_token() -> Optional[str]:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("❌ GITHUB_TOKEN is not set.")
        return None
    return token

def fetch_merged_prs(owner: str, repo: str, token: str) -> List[Dict[str, Any]]:
    merged_prs = []
    page = 1
    while True:
        data = fetch_closed_prs(owner, repo, token, page)
        if not data:
            break
        for pr in data:
            if pr.get("merged_at"):
                pr["repo_name"] = repo
                pr["owner_name"] = owner
                merged_prs.append(pr)
        page += 1
    logging.info(f"✅ {len(merged_prs)} merged PR(s) from {repo}")
    return merged_prs

def main():
    parser = argparse.ArgumentParser(description="Fetch merged PRs from GitHub")
    parser.add_argument("--owner", default="Scytale-exercise")
    parser.add_argument("--repos", default="Scytale_repo,scytale-repo2,scytale-repo3,SCytale-repo4")
    args = parser.parse_args()

    token = get_token()
    if not token:
        return

    repos = [r.strip() for r in args.repos.split(",") if r.strip()]
    all_prs = []
    for repo in repos:
        all_prs.extend(fetch_merged_prs(args.owner, repo, token))

    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/merged_prs.json", "w", encoding="utf-8") as f:
        json.dump(all_prs, f, indent=2)
    logging.info(f"💾 Saved {len(all_prs)} PR(s) to data/raw/merged_prs.json")

if __name__ == "__main__":
    main()
