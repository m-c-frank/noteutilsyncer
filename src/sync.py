import os
import re
import subprocess

def extract_related_tools_section(filename):
    with open(filename, 'r') as file:
        content = file.read()

    start_tag = "<!--START_TAG-->"
    end_tag = "<!--END_TAG-->"

    start_index = content.find(start_tag)
    end_index = content.find(end_tag)

    if start_index == -1 or end_index == -1:
        raise ValueError(f"Missing section between {start_tag} and {end_tag}")

    return content[start_index + len(start_tag):end_index].strip()

def update_repository(repo_url, related_tools_section):
    repo_name = repo_url.split('/')[-1]
    branch_name = "update-related-tools"
    
    subprocess.run(['git', 'clone', f'https://github.com/{repo_url}.git'])
    subprocess.run(['git', '-C', repo_name, 'checkout', '-b', branch_name])
    
    with open(f'{repo_name}/README.md', 'r') as file:
        content = file.read()
    pattern = r"<!--START_TAG-->.*?<!--END_TAG-->"
    replacement = f"<!--START_TAG-->\n{related_tools_section}\n<!--END_TAG-->"
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    with open(f'{repo_name}/README.md', 'w') as file:
        file.write(new_content)
    
    subprocess.run(['git', '-C', repo_name, 'add', 'README.md'])
    subprocess.run(['git', '-C', repo_name, 'commit', '-m', 'Update Related Tools section'])
    subprocess.run(['git', '-C', repo_name, 'push', 'origin', branch_name])

if __name__ == "__main__":
    related_tools_section = extract_related_tools_section('README.md')
    
    repositories = []
    if os.path.exists('READMEs'):
        for filename in os.listdir('READMEs'):
            if filename.endswith('.md'):
                with open(f'READMEs/{filename}', 'r') as file:
                    match = re.search(r'https://github.com/([a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+)', file.read())
                    if match:
                        repositories.append(match.group(1))

    for repo in repositories:
        try:
            update_repository(repo, related_tools_section)
            print(f"Updated {repo} successfully!")
        except Exception as e:
            print(f"Failed to update {repo}. Reason: {e}")
