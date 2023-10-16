def create_related_tools_section(repos):
    formatted_tools = "\n".join([f"- **[{name}](https://github.com/m-c-frank/{name})** - {description}" for name, description in repos])
    section = f"<!--START_TOKEN-->\n**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.\n\n{formatted_tools}\n<!--END_TOKEN-->"
    return section

def update_readme(repos):
    with open('README.md', 'r') as f:
        content = f.read()

    new_section = create_related_tools_section(repos)
    start_index = content.find("<!--START_TOKEN-->")
    end_index = content.find("<!--END_TOKEN-->") + len("<!--END_TOKEN-->")
    updated_content = content[:start_index] + new_section + content[end_index:]

    with open('README.md', 'w') as f:
        f.write(updated_content)

def main():
    with open("../repos.txt", "r") as f:
        repos = [(line.strip(), "") for line in f.readlines()]

    update_readme(repos)

if __name__ == "__main__":
    main()
