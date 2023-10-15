#!/usr/bin/env python3

import os
import re
import subprocess
import requests
import json

TOKEN = os.environ.get('GH_PAT')
if not TOKEN:
    raise ValueError("Missing GitHub PAT token!")

def extract_related_tools_section(filename):
    with open(filename, 'r') as file:
        content = file.read()

    related_tools_pattern = re.compile(r'## Related Tools\n\n.*?(?=##|$)', re.DOTALL)
    match = related_tools_pattern.search(content)
    if match:
        return match.group(0).strip()
    else:
        raise ValueError("Missing 'Related Tools' section")

def create_pull_request(repo_url, branch_name):
    headers = {
        'Authorization': f'token {TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': 'Update Related Tools section',
        'body': 'Automated update of the Related Tools section.',
        'head': branch_name,
        'base': 'main'
    }
    response = requests.post(f'https://api.github.com/repos/{repo_url}/pulls', headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        raise Exception(f"Failed to create pull request: {response.text}")

def update_repository(repo_url, related_tools_section):
    repo_name = repo_url.split('/')[-1]
    branch_name = "update-related-tools"
    
    # Set up git config for the GitHub Action runner
    subprocess.run(['git', 'config', '--global', 'user.name', 'GitHub Action'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])
    
    # Clone the repository
    subprocess.run(['git', 'clone', f'https://{TOKEN}@github.com/{repo_url}.git'])
    
    # Create a new branch
    subprocess.run(['git', '-C', repo_name, 'checkout', '-b', branch_name])
    
    # Replace the "Related Tools" section in README.md
    with open(f'{repo_name}/README.md', 'r') as file:
        content = file.read()
    new_content = re.sub(r'## Related Tools\n\n.*?(?=##|$)', related_tools_section, content, flags=re.DOTALL)
    with open(f'{repo_name}/README.md', 'w') as file:
        file.write(new_content)
    
    # Commit and push changes
    subprocess.run(['git', '-C', repo_name, 'add', 'README.md'])
    subprocess.run(['git', '-C', repo_name, 'commit', '-m', 'Update Related Tools section'])
    subprocess.run(['git', '-C', repo_name, 'push', 'origin', branch_name])
    
    # Create a pull request
    create_pull_request(repo_url, branch_name)


def extract_repo_url_from_readme(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Extract the first GitHub URL from the README
    match = re.search(r'https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', content)
    if match:
        return match.group(0).split("https://github.com/")[1]
    else:
        raise ValueError(f"Missing GitHub URL in {filename}")

if __name__ == "__main__":
    # Extract the "Related Tools" section from the current repository's README
    related_tools_section = extract_related_tools_section('README.md')
    
    # Dynamically fetch the list of repositories from the READMEs folder
    repositories = []
    for filename in os.listdir('READMEs'):
        if filename.endswith('.md'):
            try:
                repo = extract_repo_url_from_readme(f'READMEs/{filename}')
                repositories.append(repo)
            except ValueError as e:
                print(e)

    # Update each repository
    for repo in repositories:
        try:
            update_repository(repo, related_tools_section)
            print(f"Updated {repo} successfully!")
        except Exception as e:
            print(f"Failed to update {repo}. Reason: {e}")