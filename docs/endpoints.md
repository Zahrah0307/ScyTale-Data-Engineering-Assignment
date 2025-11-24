# GitHub API Endpoints Used

- List Pull Requests:
  `GET /repos/{owner}/{repo}/pulls?state=closed`

- List Reviews for a PR:
  `GET /repos/{owner}/{repo}/pulls/{pull_number}/reviews`

- Get Combined Status for a Commit:
  `GET /repos/{owner}/{repo}/commits/{ref}/status`
