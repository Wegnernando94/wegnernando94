#!/usr/bin/env python3
import requests
import os
import re
from datetime import datetime

# Configs
REPO = os.environ['GITHUB_REPOSITORY']  # Ex: Wegnernando94/wegnernando94
TOKEN = os.environ['GITHUB_TOKEN']
HEADERS = {'Authorization': f'token {TOKEN}', 'Accept': 'application/vnd.github.v3+json'}

def get_stats():
    """Puxa stats do GitHub API"""
    owner, repo = REPO.split('/')
    # Commits totais (aprox, via search - limite de 1000, mas ok pra perfis pessoais)
    commits_url = f"https://api.github.com/search/commits?q=repo:{REPO}+author:{owner}"
    commits_resp = requests.get(commits_url, headers=HEADERS)
    total_commits = commits_resp.json().get('total_count', 0) if commits_resp.ok else 0

    # Stars e PRs
    repo_url = f"https://api.github.com/repos/{REPO}"
    repo_resp = requests.get(repo_url, headers=HEADERS)
    stars = repo_resp.json().get('stargazers_count', 0) if repo_resp.ok else 0
    prs = repo_resp.json().get('open_issues_count', 0) if repo_resp.ok else 0  # Aprox PRs + issues

    return total_commits, stars, prs

def update_readme(total_commits, stars, prs):
    """Atualiza README com stats dinâmicas"""
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # Atualiza placeholders no README (ajuste os textos se precisar)
    content = re.sub(r'Total Commits: \d+', f'Total Commits: {total_commits}', content)
    content = re.sub(r'Stars: \d+', f'Stars: {stars}', content)
    content = re.sub(r'PRs: \d+', f'PRs: {prs}', content)

    # Adiciona/atualiza data no final
    update_line = f"\n<!-- Stats boosted on {datetime.now().strftime('%d/%m/%Y %H:%M UTC')} -->"
    content = re.sub(r'<!-- Stats boosted on .* -->', update_line, content) or content + update_line

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    commits, stars, prs = get_stats()
    print(f"Stats atualizadas: Commits={commits}, Stars={stars}, PRs={prs}")
    update_readme(commits, stars, prs)
    print("README atualizado com sucesso!")
