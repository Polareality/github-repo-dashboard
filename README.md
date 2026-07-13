\# GitHub Repo Health Dashboard



\## Project Description



GitHub Repo Health Dashboard is a Flask web app that finds the top 5 most-starred GitHub repositories created in the last two weeks and displays key health metrics for each repository.



The app uses the GitHub API to fetch repository data, issue counts, pull request counts, contributors, and a simple health status.



\## Features



\- Fetches the top 5 most-starred repositories created in the last two weeks

\- Displays repository name, star count, and GitHub URL

\- Fetches open and closed issue counts

\- Fetches open and closed pull request counts

\- Shows the top contributors for each repo

\- Calculates a health status:

&#x20; - Healthy: fewer than 10 open issues

&#x20; - Needs Attention: 10–50 open issues

&#x20; - Critical: more than 50 open issues

\- Provides a Flask API endpoint

\- Dynamically loads data into the frontend dashboard with JavaScript



\## Technologies Used



\- Python

\- Flask

\- HTML

\- CSS

\- JavaScript

\- GitHub REST API

\- requests

\- python-dotenv

\- Git and GitHub



\## Project Structure



```text

github-repo-dashboard/

├── app.py

├── fetch\_trending\_repos.py

├── requirements.txt

├── README.md

├── ARCHITECTURE\_PLAN.md

├── WIREFRAME.md

├── TESTING\_NOTES.md

├── CODE\_REVIEW.md

├── templates/

│   └── index.html

└── static/

&#x20;   ├── styles.css

&#x20;   └── script.js

