from datetime import datetime, timedelta, timezone
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

load_dotenv()

app = Flask(__name__)

GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def github_headers():
    headers = {
        "Accept": "application/vnd.github+json"
    }

    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    return headers


def get_date_two_weeks_ago():
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)
    return two_weeks_ago.strftime("%Y-%m-%d")


def github_get(url, params=None):
    response = requests.get(
        url,
        headers=github_headers(),
        params=params,
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def search_count(query):
    url = f"{GITHUB_API_BASE}/search/issues"
    data = github_get(url, params={"q": query, "per_page": 1})
    return data.get("total_count", 0)


def fetch_repo_metrics(owner, repo):
    try:
        open_issues = search_count(f"repo:{owner}/{repo} is:issue is:open")
        closed_issues = search_count(f"repo:{owner}/{repo} is:issue is:closed")
        open_prs = search_count(f"repo:{owner}/{repo} is:pr is:open")
        closed_prs = search_count(f"repo:{owner}/{repo} is:pr is:closed")

        contributors_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contributors"
        contributors_data = github_get(contributors_url, params={"per_page": 5})

        contributors = []
        for contributor in contributors_data:
            contributors.append({
                "username": contributor.get("login", "unknown"),
                "contributions": contributor.get("contributions", 0),
                "profile_url": contributor.get("html_url", "")
            })

        return {
            "open_issues": open_issues,
            "closed_issues": closed_issues,
            "open_prs": open_prs,
            "closed_prs": closed_prs,
            "contributors": contributors
        }

    except requests.exceptions.RequestException:
        return {
            "open_issues": 0,
            "closed_issues": 0,
            "open_prs": 0,
            "closed_prs": 0,
            "contributors": []
        }


def calculate_health_status(open_issues):
    if open_issues < 10:
        return "healthy"
    elif open_issues <= 50:
        return "needs_attention"
    else:
        return "critical"


def fetch_trending_repositories():
    date = get_date_two_weeks_ago()

    url = f"{GITHUB_API_BASE}/search/repositories"

    params = {
        "q": f"created:>{date}",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }

    data = github_get(url, params=params)

    repositories = []

    for repo in data.get("items", []):
        full_name = repo.get("full_name", "")
        owner, repo_name = full_name.split("/", 1)

        metrics = fetch_repo_metrics(owner, repo_name)
        health_status = calculate_health_status(metrics["open_issues"])

        repositories.append({
            "name": full_name,
            "stars": repo.get("stargazers_count", 0),
            "url": repo.get("html_url", ""),
            **metrics,
            "health_status": health_status
        })

    return repositories


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/trending")
def api_trending():
    try:
        repositories = fetch_trending_repositories()

        return jsonify({
            "status": "success",
            "count": len(repositories),
            "repositories": repositories
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({
            "status": "error",
            "message": "GitHub API request timed out."
        }), 504

    except requests.exceptions.HTTPError as error:
        status_code = error.response.status_code if error.response else 502

        return jsonify({
            "status": "error",
            "message": "GitHub API returned an HTTP error.",
            "details": str(error)
        }), status_code

    except requests.exceptions.RequestException as error:
        return jsonify({
            "status": "error",
            "message": "Could not connect to the GitHub API.",
            "details": str(error)
        }), 502

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Unexpected server error.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)