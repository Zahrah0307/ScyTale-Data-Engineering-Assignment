# Scytale Modular Assignment

## How to Run
1. Install dependencies:
```bash
pip install requests
```
2. Set your GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
```
3. Run the scripts:
```bash
python extract.py
python transform.py
```

## Future-Proof Tips
- Modular design: `github_api.py` centralizes API calls for easy updates.
- Add unit tests for each module.
- Consider using `PyGithub` library for more robust API handling.
- Implement caching or GraphQL for performance.
