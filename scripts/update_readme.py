import os

def create_related_tools_section(repo_names):
    formatted_links = "\n".join([f"- **[{name}](https://github.com/m-c-frank/{name})**" for name in repo_names])
    section = f"\n{formatted_links}\n"
    return section

def replace_token_with_links(repo_names):
    readme_path = "README.md"
    with open(readme_path, 'r') as file:
        content = file.read()

    start_token = "<!--START_TOKEN-->"
    end_token = "<!--END_TOKEN-->"
    
    start_index = content.find(start_token)
    end_index = content.find(end_token)

    # If tokens are not found, just return without making changes
    if start_index == -1 or end_index == -1:
        return

    new_section = create_related_tools_section(repo_names)
    updated_content = content[:start_index+len(start_token)] + new_section + content[end_index:]

    with open(readme_path, 'w') as file:
        file.write(updated_content)

def main():
    with open("../repos.txt", "r") as f:
        repo_names = [line.strip() for line in f.readlines()]

    replace_token_with_links(repo_names)

if __name__ == "__main__":
    main()
