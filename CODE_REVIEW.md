\# Code Review Notes



\## Files Reviewed



\- app.py

\- templates/index.html

\- static/styles.css

\- static/script.js



\## What Works



The backend exposes a working `/api/trending` endpoint that fetches the top 5 most-starred repositories created in the last two weeks.



The endpoint now returns:



\- repo name

\- star count

\- GitHub URL

\- open/closed issues

\- open/closed pull requests

\- top contributors

\- health status



The frontend fetches data from `/api/trending` on page load and dynamically creates repository cards.



\## Testing



Tested backend with:



```cmd

curl.exe http://127.0.0.1:5000/api/trending

