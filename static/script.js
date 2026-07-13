async function fetchTrendingRepos() {
    const grid = document.getElementById("repo-grid");
    const statusMessage = document.getElementById("status-message");

    try {
        statusMessage.textContent = "Loading repository data...";

        const response = await fetch("/api/trending");

        if (!response.ok) {
            throw new Error("Failed to load repository data.");
        }

        const data = await response.json();

        grid.innerHTML = "";

        data.repositories.forEach(repo => {
            grid.appendChild(createRepoCard(repo));
        });

        statusMessage.textContent = `Loaded ${data.count} trending repositories.`;

    } catch (error) {
        statusMessage.textContent = "Error loading repository data.";
        grid.innerHTML = `<p class="error-message">${error.message}</p>`;
    }
}

function getHealthClass(status) {
    if (status === "healthy") {
        return "healthy";
    }

    if (status === "needs_attention") {
        return "warning";
    }

    return "critical";
}

function formatHealthStatus(status) {
    if (status === "healthy") {
        return "● HEALTHY";
    }

    if (status === "needs_attention") {
        return "● NEEDS ATTENTION";
    }

    return "● CRITICAL";
}

function createRepoCard(repo) {
    const healthClass = getHealthClass(repo.health_status);

    const contributors = repo.contributors.length
        ? repo.contributors.map(contributor => `
            <li>
                <a href="${contributor.profile_url}" target="_blank">
                    ${contributor.username}
                </a>
                — ${contributor.contributions} contributions
            </li>
        `).join("")
        : "<li>No contributor data available</li>";

    const card = document.createElement("article");
    card.className = `repo-card ${healthClass}-border`;

    card.innerHTML = `
        <div class="card-header">
            <div>
                <h2>${repo.name}</h2>
                <p class="stars">★ ${repo.stars.toLocaleString()} stars</p>
                <a class="repo-link" href="${repo.url}" target="_blank">View on GitHub</a>
            </div>

            <span class="badge ${healthClass}">
                ${formatHealthStatus(repo.health_status)}
            </span>
        </div>

        <div class="metrics">
            <div class="metric-box">
                <p>ISSUES</p>
                <strong>${repo.open_issues}</strong>
                <span>open</span>
                <strong class="muted">${repo.closed_issues}</strong>
                <span>closed</span>
            </div>

            <div class="metric-box">
                <p>PULL REQUESTS</p>
                <strong>${repo.open_prs}</strong>
                <span>open</span>
                <strong class="muted">${repo.closed_prs}</strong>
                <span>closed</span>
            </div>
        </div>

        <div class="contributors">
            <p>TOP CONTRIBUTORS</p>
            <ul>
                ${contributors}
            </ul>
        </div>
    `;

    return card;
}

document.addEventListener("DOMContentLoaded", fetchTrendingRepos);