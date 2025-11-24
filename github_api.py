"""github_api.py - Helper functions for GitHub API calls"""
import requests

# Base URL for GitHub's API
GITHUB_API = "https://api.github.com"

# Function to create headers for authentication using my GitHub token
def get_headers(token: str) -> dict:
    return {"Authorization": f"token {token}"}

# Function to get all closed PRs from a repo
def fetch_closed_prs(owner: str, repo: str, token: str, page: int = 1) -> list:
    """Fetch closed PRs for a given repo and page."""
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls"
    params = {"state": "closed", "per_page": 100, "page": page}
    resp = requests.get(url, headers=get_headers(token), params=params)
    
	# If the request fails show an error
	if resp.status_code != 200:
        raise Exception(f"Failed to fetch PRs: {resp.status_code} {resp.text}")
     
	 # Return the PRs as a list
	return resp.json()

# Function to get all reviews for a specific pull request
def fetch_reviews(owner: str, repo: str, pr_number: int, token: str) -> list:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    resp = requests.get(url, headers=get_headers(token))
    
	# Return reviews if successful or else return empty list
	return resp.json() if resp.status_code == 200 else []

# Function to check the status of a specific commit
def fetch_commit_status(owner: str, repo: str, sha: str, token: str) -> dict:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{sha}/status"
    resp = requests.get(url, headers=get_headers(token))
    
	# Return status if successful or else return empty dict
	return resp.json() if resp.status_code == 200 else {}
