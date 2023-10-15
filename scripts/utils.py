import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"


def fetch_gist_content(url=GIST_URL):
    """
    Fetch the content of the gist.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def split_gist_into_repos(gist_content):
    """
    Split the gist content into a list of repo names.
    """
    return gist_content.strip().split('\n')


def format_related_tool(repo_name):
    """
    Format a single repo name into the "Related Tools" section format.
    """
    return f"- **[{repo_name}](https://github.com/m-c-frank/{repo_name})**"


def create_related_tools_section(repo_names):
    """
    Create the "Related Tools" section using the given repo names.
    """
    formatted_tools = "\n".join([format_related_tool(name) for name in repo_names])
    section = f"<!--START_TAG-->\n**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.\n\n{formatted_tools}\n<!--END_TAG-->"
    return section


def extract_section_from_content(content, start_tag="<!--START_TAG-->", end_tag="<!--END_TAG-->"):
    """
    Extract content between the given start and end tags.
    """
    start_index = content.find(start_tag) + len(start_tag)
    end_index = content.find(end_tag)
    return content[start_index:end_index].strip()


def replace_section_in_content(content, new_section, start_tag="<!--START_TAG-->", end_tag="<!--END_TAG-->"):
    """
    Replace the content between the given start and end tags with the new_section.
    """
    start_index = content.find(start_tag)
    end_index = content.find(end_tag) + len(end_tag)
    return content[:start_index] + new_section + content[end_index:]


def check_and_update_readme():
    """
    Check if the "Related Tools" section in the README has changed, 
    and if so, update the README and return True.
    If not, return False.
    """
    # Fetch the content of the current README (this could be done using file operations)
    with open('README.md', 'r') as f:
        current_readme_content = f.read()

    current_section = extract_section_from_content(current_readme_content)
    
    repo_names = split_gist_into_repos(fetch_gist_content())
    new_section = create_related_tools_section(repo_names)
    
    if current_section != new_section:
        updated_readme_content = replace_section_in_content(current_readme_content, new_section)
        
        with open('README.md', 'w') as f:
            f.write(updated_readme_content)
        
        return True
    
    return False
