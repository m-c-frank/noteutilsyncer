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


def update_current_readme(repo_names):
    with open('README.md', 'r') as f:
        content = f.read()

    new_section = create_related_tools_section(repo_names)
    start_index = content.find("<!--START_TAG-->")
    end_index = content.find("<!--END_TAG-->") + len("<!--END_TAG-->")
    updated_content = content[:start_index] + new_section + content[end_index:]

    with open('README.md', 'w') as f:
        f.write(updated_content)


def main():
    repo_names = fetch_gist_content()
    update_current_readme(repo_names)

    # Excluding the current repository from the list
    repo_names.remove("noteutilsyncer")
    for repo in repo_names:
        print(repo)


if __name__ == "__main__":
    main()
