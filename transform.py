
"""transform.py - Analyze PRs and generate CSV with summary"""
import os
import json
import csv
import logging
from github_api import fetch_reviews, fetch_commit_status

logging.basicConfig(level=logging.INFO, format="%(message)s")

def get_token():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        logging.error("❌ GITHUB_TOKEN is not set.")
        raise SystemExit(1)
    return token

def main():
    token = get_token()
    raw_path = "data/raw/merged_prs.json"
    if not os.path.exists(raw_path):
        logging.error("❌ merged_prs.json not found. Run extract.py first.")
        return

    with open(raw_path, "r", encoding="utf-8") as f:
        prs = json.load(f)

    rows = []
    summary = {}
    for pr in prs:
        pr_number = pr["number"]
        title = pr.get("title", "")
        author = pr.get("user", {}).get("login", "")
        merged_at = pr.get("merged_at", "")
        owner = pr.get("owner_name", "")
        repo = pr.get("repo_name", "")

        reviews = fetch_reviews(owner, repo, pr_number, token)
        cr_passed = any(r.get("state") == "APPROVED" for r in reviews)

        commit_sha = pr.get("merge_commit_sha")
        checks_passed = False
        if commit_sha:
            status = fetch_commit_status(owner, repo, commit_sha, token)
            checks_passed = status.get("state") == "success"

        rows.append([pr_number, title, author, merged_at, cr_passed, checks_passed, repo])

        # Update summary
        if repo not in summary:
            summary[repo] = {"total": 0, "approved": 0, "checks": 0}
        summary[repo]["total"] += 1
        if cr_passed:
            summary[repo]["approved"] += 1
        if checks_passed:
            summary[repo]["checks"] += 1

    os.makedirs("data/processed", exist_ok=True)
    out_path = "data/processed/report.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PR_Number", "Title", "Author", "Merged_At", "CR_PASSED", "CHECKS_PASSED", "Repo_Name"])
        writer.writerows(rows)

    logging.info(f"✅ Report saved to {out_path}")
    logging.info("\n📊 Summary Report:")
    for repo, stats in summary.items():
        logging.info(f"  {repo}: Total={stats['total']}, Approved={stats['approved']}, Checks Passed={stats['checks']}")

if __name__ == "__main__":
    main()
