import os
import re
import subprocess
import requests
import json

# Constants
START_TAG = "<!--START_TAG-->"
END_TAG = "<!--END_TAG-->"
GH_PAT = os.environ.get('GH_PAT')


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()


def write_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)


def extract_section(content, start_tag=START_TAG, end_tag=END_TAG):
    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Missing section between {start_tag} and {end_tag}")

    return content[start_index + len(start_tag):end_index].strip()


def replace_section(content, start_tag, end_tag, new_section):
    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Missing section between {start_tag} and {end_tag}")

    # Extract the content before the start tag, the new section, and the content after the end tag
    return content[:start_index] + new_section + content[end_index + len(end_tag):]



def git_config():
    subprocess.run(['git', 'config', '--global', 'user.name', 'GitHub Action'])
    subprocess.run(['git', 'config', '--global', 'user.email', 'action@github.com'])


def clone_and_update_repo(repo_url, new_section):
    repo_name = repo_url.split('/')[-1]
    branch_name = "update-related-tools"
    
    subprocess.run(['git', 'clone', f'https://github.com/{repo_url}.git'])
    subprocess.run(['git', '-C', repo_name, 'checkout', '-b', branch_name])
    
    content = read_file(f'{repo_name}/README.md')
    updated_content = replace_section(content, "<!--START_TAG-->", "<!--END_TAG-->", new_section)
    write_file(f'{repo_name}/README.md', updated_content)
    
    subprocess.run(['git', '-C', repo_name, 'add', 'README.md'])
    subprocess.run(['git', '-C', repo_name, 'commit', '-m', 'Update Related Tools section'])
    subprocess.run(['git', '-C', repo_name, 'push', 'origin', branch_name])


def create_pull_request(repo_url, branch_name, token=GH_PAT):
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    data = {
        'title': 'Update Related Tools section',
        'body': 'Automated update of the Related Tools section.',
        'head': branch_name,
        'base': 'main'
    }
    response = requests.post(f'https://api.github.com/repos/{repo_url}/pulls', headers=headers, data=json.dumps(data))
    response.raise_for_status()


def extract_repo_urls_from_directory(directory='READMEs'):
    repositories = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            content = read_file(f'{directory}/{filename}')
            match = re.search(r'https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', content)
            if match:
                repositories.append(match.group(0).split("https://github.com/")[1])
    return repositories


if __name__ == "__main__":
    if not GH_PAT:
        raise ValueError("Missing GitHub PAT token!")

    content = read_file('README.md')
    related_tools_section = extract_section(content)
    
    repositories = extract_repo_urls_from_directory()

    git_config()

    for repo in repositories:
        try:
            clone_and_update_repo(repo, related_tools_section)
            create_pull_request(repo, "update-related-tools")
            print(f"Updated {repo} successfully!")
        except Exception as e:
            print(f"Failed to update {repo}. Reason: {e}")
