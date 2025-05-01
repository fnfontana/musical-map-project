#!/usr/bin/env python3
import os
import json
from ghapi.core import GhApi  # type: ignore


def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        raise EnvironmentError(
            "GH_TOKEN environment variable is not set. "
            "Please set it before running the script."
        )
    api = GhApi(owner="fnfontana", repo="musical-map-project", token=token)

    # Issues (filtra PRs) - handle pagination to fetch all issues
    all_issues = []
    page = 1
    while True:
        issues_page = api.issues.list_for_repo(
            state="all", page=page, per_page=100
        )
        if not issues_page:
            break
        all_issues.extend(issues_page)
        page += 1
    issues = [i for i in all_issues if not getattr(i, "pull_request", None)]
    tasks = []
    for i in issues:
        labels = [label.name for label in i.labels]
        comp = next(
            (
                label
                for label in labels
                if label
                in [
                    "autonomous",
                    "interface",
                    "refactor",
                    "data",
                    "monitoring",
                ]
            ),
            "other",
        )
        status = next(
            (
                label
                for label in labels
                if label in ["backlog", "in-progress", "completed"]
            ),
            None,
        )
        status = status or ("completed" if i.state == "closed" else "pending")
        tasks.append(
            {
                "title": i.title,
                "component": comp,
                "status": status,
                "url": i.html_url,
            }
        )

    # Milestones
    ms = api.repos.list_milestones_for_repo(state="all", per_page=10)
    milestones = []
    milestones.extend(
        {
            "title": m.title,
            "state": m.state,
            "open_issues": m.open_issues,
            "closed_issues": m.closed_issues,
            "due_on": m.due_on,
        }
        for m in ms
    )
    # Commits count (página única de 100)
    commits = api.repos.list_commits(per_page=100)
    commit_count = len(commits)

    output = {
        "issues": tasks,
        "milestones": milestones,
        "commitsCount": commit_count,
    }
    output_path = (
        "docs/data.json"
    )
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
