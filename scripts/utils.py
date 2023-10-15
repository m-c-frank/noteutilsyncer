import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw"


def fetch_gist_content():
    """
    Fetch the content of the gist.
    """
    response = requests.get(GIST_URL)
    response.raise_for_status()
    return response.text


def format_related_tools_section(gist_content):
    """
    Format the gist content into the "Related Tools" section format.
    """
    repo_names = gist_content.strip().split('\n')
    formatted_tools = "\n".join([f"- **[{name}](https://github.com/m-c-frank/{name})**" for name in repo_names])
    
    section = f"<!--START_TAG-->\n**Note Utilities Ecosystem**: A suite of tools designed to streamline and enhance your note-taking and information processing workflows.\n\n{formatted_tools}\n<!--END_TAG-->"
    
    return section


def extract_current_related_tools_section(readme_content):
    """
    Extract the current "Related Tools" section from the given README content.
    """
    start_tag = "<!--START_TAG-->"
    end_tag = "<!--END_TAG-->"
    
    start_index = readme_content.find(start_tag) + len(start_tag)
    end_index = readme_content.find(end_tag)
    
    return readme_content[start_index:end_index].strip()


def check_and_update_readme():
    """
    Check if the "Related Tools" section in the README has changed, 
    and if so, update the README and return True.
    If not, return False.
    """
    # Fetch the content of the current README (this could be done using file operations)
    with open('README.md', 'r') as f:
        current_readme_content = f.read()
    
    current_section = extract_current_related_tools_section(current_readme_content)
    new_section = format_related_tools_section(fetch_gist_content())
    
    if current_section != new_section:
        updated_readme_content = current_readme_content.replace(current_section, new_section)
        
        with open('README.md', 'w') as f:
            f.write(updated_readme_content)
        
        return True
    
    return False

