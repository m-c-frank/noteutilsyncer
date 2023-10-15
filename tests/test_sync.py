import pytest
from src.sync import (read_file, write_file, extract_section, replace_section,
                      git_config, clone_and_update_repo, create_pull_request,
                      extract_repo_urls_from_directory)

# Sample content for mock README.md
MOCK_CONTENT = """
# Project Title

## Features
- Feature A
- Feature B

## Related Tools
<!--START_TAG-->
- Tool A (https://github.com/user/toolA)
- Tool B (https://github.com/user/toolB)
<!--END_TAG-->

## License
MIT License
"""

def test_read_file(mocker):
    mocker.patch('builtins.open', mocker.mock_open(read_data=MOCK_CONTENT))
    content = read_file("mock_readme.md")
    assert "Project Title" in content

def test_write_file(mocker):
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    write_file("mock_readme.md", MOCK_CONTENT)
    mock_open.assert_called_once_with("mock_readme.md", "w")

def test_extract_section():
    section = extract_section(MOCK_CONTENT, "<!--START_TAG-->", "<!--END_TAG-->")
    assert "Tool A" in section
    assert "Tool B" in section

def test_replace_section():
    new_section = """
<!--START_TAG-->
- Tool C (https://github.com/user/toolC)
<!--END_TAG-->
"""
    updated_content = replace_section(MOCK_CONTENT, "<!--START_TAG-->", "<!--END_TAG-->", new_section)
    assert "Tool C" in updated_content
    assert "Tool A" not in updated_content
    assert "Tool B" not in updated_content


def test_git_config(mocker):
    mock_subprocess = mocker.patch('subprocess.run')
    git_config()
    assert mock_subprocess.call_count == 2

def test_clone_and_update_repo(mocker):
    mock_subprocess = mocker.patch('subprocess.run')
    mock_read_file = mocker.patch('src.sync.read_file', return_value=MOCK_CONTENT)
    mock_write_file = mocker.patch('src.sync.write_file')
    
    clone_and_update_repo("user/repo", "## Related Tools\n- Tool A\n- Tool B")
    
    assert mock_subprocess.call_count == 5
    mock_read_file.assert_called_once()
    mock_write_file.assert_called_once()

def test_create_pull_request(mocker):
    mock_requests = mocker.patch('requests.post')
    mock_response = mocker.MagicMock()
    mock_response.status_code = 201
    mock_requests.return_value = mock_response
    
    create_pull_request("user/repo", "branch_name", "mock_token")
    mock_requests.assert_called_once()

def test_extract_repo_urls_from_directory(mocker):
    mock_os = mocker.patch('os.listdir', return_value=['mock_readme1.md', 'mock_readme2.md'])
    mock_read_file = mocker.patch('src.sync.read_file', return_value=MOCK_CONTENT)
    
    repo_urls = extract_repo_urls_from_directory('READMEs')
    
    assert len(repo_urls) == 2
    assert "user/toolA" in repo_urls
