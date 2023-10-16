import pytest
from noteutilsyncer.update_readme import create_related_tools_section, update_readme

def test_create_related_tools_section():
    repos = [('repo1', 'Description for repo1'), ('repo2', 'Description for repo2')]
    result = create_related_tools_section(repos)
    assert '**[repo1](https://github.com/m-c-frank/repo1)** - Description for repo1' in result
    assert '**[repo2](https://github.com/m-c-frank/repo2)** - Description for repo2' in result

def test_update_readme(mocker):
    # Mock the content of README.md
    mock_readme_content = 'Some initial content\n<!--START_TOKEN-->\nOld related tools section\n<!--END_TOKEN-->\nSome other content'
    
    # Mock the open function to read our mock content and capture what's written
    mock_open_instance = mocker.mock_open(read_data=mock_readme_content)
    mocker.patch('builtins.open', mock_open_instance)

    repos = [('repo1', 'Description for repo1'), ('repo2', 'Description for repo2')]
    update_readme(repos)

    # Check what was written to the file
    handle = mock_open_instance()
    written_content = handle.write.call_args[0][0]

    assert '**[repo1](https://github.com/m-c-frank/repo1)** - Description for repo1' in written_content
    assert '**[repo2](https://github.com/m-c-frank/repo2)** - Description for repo2' in written_content
    assert 'Some initial content' in written_content
    assert 'Some other content' in written_content
    assert 'Old related tools section' not in written_content

