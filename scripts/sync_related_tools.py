import os
import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"


def fetch_gist_content():
    response = requests.get(GIST_URL)
    response.raise_for_status()
    return response.text.strip().split('\n')


def create_related_tools_section(repo_names):
    formatted_tools = "\n".join([f"- **[{name}](https://github.com/m-c-frank/{name})**" for name in repo_names])
    section = f"<!--START_TAG-->\n**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.\n\n{formatted_tools}\n<!--END_TAG-->"
    return section

def replace_token_with_links(repo_path, repo_names):
    readme_path = os.path.join(repo_path, "README.md")
    with open(readme_path, 'r') as file:
        content = file.read()
    
    if "<SPECIAL_TOKEN>" not in content:
        return

    formatted_links = "\n".join([f"- **[{name}](https://github.com/m-c-frank/{name})**" for name in repo_names])
    updated_content = content.replace("<SPECIAL_TOKEN>", formatted_links)

    with open(readme_path, 'w') as file:
        file.write(updated_content)

def main():
    repo_names = fetch_gist_content()
    
    # Write the repo names to repos.txt
    with open("repos.txt", "w") as f:
        for repo in repo_names:
            f.write(f"{repo}\n")

    for repo in repo_names:
        repo_path = os.path.join("..", repo)
        replace_token_with_links(repo_path, repo_names)


if __name__ == "__main__":
    main()
