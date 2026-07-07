import requests
from datetime import datetime, timedelta


def get_top_repos_last_two_weeks(per_page=5):
    """
    Fetch the top starred GitHub repositories created in the last two weeks.

    Returns:
        list of dicts with repo info, or None if the request failed.
    """
    # Step 1: Calculate the date from two weeks ago
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    date_str = two_weeks_ago.strftime("%Y-%m-%d")

    # Step 2: Construct the GitHub search query
    # "created:>DATE" filters repos created after that date
    query = f"created:>{date_str}"

    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": per_page,
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # Step 3: Make the request, with error handling
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # raises HTTPError for 4xx/5xx responses
    except requests.exceptions.Timeout:
        print("Error: The request to GitHub timed out.")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"Error: GitHub API returned an error: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: A network problem occurred: {e}")
        return None

    # Step 4: Parse the JSON response
    try:
        data = response.json()
    except ValueError:
        print("Error: Could not parse JSON response.")
        return None

    items = data.get("items", [])

    # Step 5: Extract the relevant fields
    top_repos = [
        {
            "name": repo["full_name"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
            "created_at": repo["created_at"],
        }
        for repo in items
    ]

    return top_repos


if __name__ == "__main__":
    repos = get_top_repos_last_two_weeks()
    if repos:
        for i, repo in enumerate(repos, start=1):
            print(f"{i}. {repo['name']} — {repo['stars']} stars ({repo['url']})")
    else:
        print("No results returned.")