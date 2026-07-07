from flask import Flask, jsonify, render_template
from datetime import datetime, timedelta, timezone
import requests

app = Flask(__name__)


def get_date_two_weeks_ago():
    two_weeks_ago = datetime.now(timezone.utc) - timedelta(days=14)
    return two_weeks_ago.strftime("%Y-%m-%d")


def fetch_trending_repositories():
    date = get_date_two_weeks_ago()

    url = "https://api.github.com/search/repositories"

    params = {
        "q": f"created:>{date}",
        "sort": "stars",
        "order": "desc",
        "per_page": 5
    }

    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()

    repos = []
    for repo in data.get("items", []):
        repos.append({
            "name": repo.get("full_name"),
            "stars": repo.get("stargazers_count"),
            "url": repo.get("html_url")
        })

    return repos


@app.route("/")
def dashboard():
    return render_template("index.html")


@app.route("/api/trending")
def api_trending():
    try:
        repos = fetch_trending_repositories()

        return jsonify({
            "status": "success",
            "count": len(repos),
            "repositories": repos
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

    except ValueError:
        return jsonify({
            "status": "error",
            "message": "GitHub API returned invalid JSON."
        }), 502

    except Exception as error:
        return jsonify({
            "status": "error",
            "message": "Unexpected server error.",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)