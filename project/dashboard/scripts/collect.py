#!/usr/bin/env python3
import os
import json
from ghapi import GhApi

def main():
    token = os.environ.get('GH_TOKEN')
    if not token:
        raise EnvironmentError("GH_TOKEN environment variable is not set. Please set it before running the script.")
    api = GhApi(owner='fnfontana', repo='musical-map-project', token=token)

    # Issues (filtra PRs)
    all_issues = api.issues.list_for_repo(state='all', per_page=100)
    issues = [i for i in all_issues if not getattr(i, 'pull_request', None)]
    tasks = []
    for i in issues:
        labels = [l.name for l in i.labels]
        comp = next((l for l in labels if l in ['autonomous','interface','refactor','data','monitoring']), 'other')
        status = next((l for l in labels if l in ['backlog','in-progress','completed']), None)
        status = status or ('completed' if i.state == 'closed' else 'pending')
        tasks.append({
            'title': i.title,
            'component': comp,
            'status': status,
            'url': i.html_url
        })

    # Milestones
    ms = api.issues.list_milestones_for_repo(state='all', per_page=10)
    milestones = []
    for m in ms:
        milestones.append({
            'title': m.title,
            'state': m.state,
            'open_issues': m.open_issues,
            'closed_issues': m.closed_issues,
            'due_on': m.due_on
        })

    # Commits count (página única de 100)
    commits = api.repos.list_commits(per_page=100)
    commit_count = len(commits)

    output = {
        'issues': tasks,
        'milestones': milestones,
        'commitsCount': commit_count
    }
    print(json.dumps(output))

if __name__ == '__main__':
    main()