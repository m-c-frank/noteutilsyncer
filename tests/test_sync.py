import pytest
from src.sync import extract_related_tools_section, update_repository, create_pull_request, extract_repo_url_from_readme
import os
import requests
import subprocess

# Adjusted mock content for README.md
MOCK_CONTENT = """
# Project Title

## Features
- Feature A
- Feature B

## Related Tools

- Tool A (https://github.com/user/toolA)
- Tool B (https://github.com/user/toolB)

## License
MIT License
"""

def test_extract_related_tools_section():
    with open("mock_readme.md", "w") as f:
        f.write(MOCK_CONTENT)

    section = extract_related_tools_section("mock_readme.md")
    assert section == "## Related Tools\n\n- Tool A (https://github.com/user/toolA)\n- Tool B (https://github.com/user/toolB)"
    os.remove("mock_readme.md")

def test_extract_repo_url_from_readme():
    with open("mock_readme.md", "w") as f:
        f.write(MOCK_CONTENT)

    repo_url = extract_repo_url_from_readme("mock_readme.md")
    assert repo_url == "user/toolA"
    os.remove("mock_readme.md")

@pytest.mark.parametrize("content, expected_url", [
    ("""
    ## Related Tools
    - Tool A (https://github.com/user/toolA)
    """, "user/toolA"),
    ("""
    ## Related Tools
    - Tool B (https://github.com/user/toolB)
    """, "user/toolB")
])
def test_extract_repo_url_from_readme_parametrized(content, expected_url):
    with open("mock_readme.md", "w") as f:
        f.write(content)

    repo_url = extract_repo_url_from_readme("mock_readme.md")
    assert repo_url == expected_url
    os.remove("mock_readme.md")


def test_create_pull_request(mocker):
    mock_post = mocker.patch('requests.post')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response
    
    create_pull_request("user/repo", "branch_name", "mock_token")
    
    # Adjusted assertion
    mock_post.assert_called_once()

def test_update_repository(mocker):
    mocker.patch('subprocess.run')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 201
    mocker.patch('requests.post', return_value=mock_response)

    os.environ['GH_PAT'] = 'mock_token'
    if not os.path.exists("repo"):
        os.mkdir("repo")
    with open("repo/README.md", "w") as f:
        f.write(MOCK_CONTENT)
    update_repository("user/repo", "## Related Tools\n- Tool A\n- Tool B")
    os.remove("repo/README.md")

    # Assert that subprocess.run was called (indicating git operations were performed)
    assert subprocess.run.call_count > 0

    # Cleanup
    del os.environ['GH_PAT']