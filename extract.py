"""extract.py - Fetch merged PRs and save to data/raw"""
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import argparse
from github_api import fetch_closed_prs 

# sets up logging so we can see msgs when the code runs
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Get GitHub token from environment variable
def get_token() -> Optional[str]:
    token = os.getenv("GITHUB_TOKEN") 
    if not token:
        logging.error("❌ GITHUB_TOKEN is not set.") # Warn if token not found
        return None
    return token 

 # Fetch all merged PRs from a repo
def fetch_merged_prs(owner: str, repo: str, token: str) -> List[Dict[str, Any]]:
    merged_prs = []
    page = 1 # GitHub API returns results in pages
    while True:
        data = fetch_closed_prs(owner, repo, token, page)
        if not data:  # Stop if no more PRs
            break
        for pr in data:
            if pr.get("merged_at"):  # Only keep PRs that were merged
                pr["repo_name"] = repo # Save repo name
                pr["owner_name"] = owner # Save owner name
                merged_prs.append(pr) # Add to final list
        page += 1 # Go to next page
    logging.info(f"✅ {len(merged_prs)} merged PR(s) from {repo}")
    return merged_prs

def main():
 # Set up command line arguments
    parser = argparse.ArgumentParser(description="Fetch merged PRs from GitHub")
    parser.add_argument("--owner", default="Scytale-exercise")
    parser.add_argument("--repos", default="Scytale_repo,scytale-repo2,scytale-repo3,SCytale-repo4")
    args = parser.parse_args()

    token = get_token() # Get token from environment
    if not token:
        return # Stop if token not found

# Convert comma-separated repo names into a list
    repos = [r.strip() for r in args.repos.split(",") if r.strip()]
    all_prs = []
    for repo in repos:
        all_prs.extend(fetch_merged_prs(args.owner, repo, token))

# Make folder if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)
    with open("data/raw/merged_prs.json", "w", encoding="utf-8") as f:
        json.dump(all_prs, f, indent=2)
    logging.info(f"💾 Saved {len(all_prs)} PR(s) to data/raw/merged_prs.json")

# Run the main function if this file is executed
if __name__ == "__main__":
    main()
