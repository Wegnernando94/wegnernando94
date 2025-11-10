#!/usr/bin/env python3
import requests
import os
import re
from datetime import datetime

# Configs do GitHub
REPO = os.environ.get('GITHUB_REPOSITORY', 'Wegnernando94/wegnernando94')
TOKEN = os.environ.get('GITHUB_TOKEN')
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

def get_stats():
    """Busca stats reais do GitHub API"""
    owner, repo_name = REPO.split('/')
    try:
        # Stats do repo
        repo_url = f"https://api.github.com/repos/{REPO}"
        repo_resp = requests.get(repo_url, headers=HEADERS)
        if repo_resp.ok:
            data = repo_resp.json()
            stars = data.get('stargazers_count', 0)
            forks = data.get('forks_count', 0)
            open_issues = data.get('open_issues_count', 0)  # Issues + PRs abertos

        # Commits totais (aprox via search, limite 1000)
        commits_url = f"https://api.github.com/search/commits?q=repo:{REPO}+author:{owner}"
        commits_resp = requests.get(commits_url, headers=HEADERS)
        total_commits = commits_resp.json().get('total_count', 0) if commits_resp.ok else 0

        return total_commits, stars, forks, open_issues
    except Exception as e:
        print(f"Erro na API: {e}")
        return 0, 0, 0, 0

def update_readme(commits, stars, forks, issues):
    """Atualiza README com stats e data"""
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()

        # Atualiza placeholders (ajuste se seus textos forem diferentes)
        content = re.sub(r'Total Commits: \d+', f'Total Commits: {commits}', content)
        content = re.sub(r'Stars: \d+', f'Stars: {stars}', content)
        content = re.sub(r'Forks: \d+', f'Forks: {forks}', content)
        content = re.sub(r'Open Issues/PRs: \d+', f'Open Issues/PRs: {issues}', content)

        # Data de boost no final (escondida em comentário)
        update_line = f"\n<!-- Stats boosted on {datetime.now().strftime('%d/%m/%Y %H:%M UTC')} -->"
        if '<!-- Stats boosted on' not in content:
            content += update_line

        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        print("README atualizado!")
    except Exception as e:
        print(f"Erro ao atualizar README: {e}")

if __name__ == '__main__':
    stats = get_stats()
    print(f"Stats: Commits={stats[0]}, Stars={stats[1]}, Forks={stats[2]}, Issues/PRs={stats[3]}")
    update_readme(*stats)
