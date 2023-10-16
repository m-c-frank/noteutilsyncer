import pytest
from noteutilsyncer.fetch_gist_repos import fetch_gist_content

def test_fetch_gist_content(mocker):
    mock_response = mocker.Mock()
    mock_response.text = """
workflowlibrary,'Centralizes and synchronizes the "Related Tools" section across the ecosystem.'
noteutilsyncer,'A centralized tool that automates the synchronization of the "Related Tools" section across READMEs in the noteutils ecosystem.'
conceptsplitter,'Extract atomic concepts from a given text using the OpenAI API.'
textdownloader,'A browser extension to automatically generate text dumps for processing.'
"""
    mocker.patch('requests.get', return_value=mock_response)
    
    repos = fetch_gist_content()
    
    # Validate the parsed data
    assert repos[0] == ('workflowlibrary', 'Centralizes and synchronizes the "Related Tools" section across the ecosystem.')
    assert repos[1] == ('noteutilsyncer', 'A centralized tool that automates the synchronization of the "Related Tools" section across READMEs in the noteutils ecosystem.')
    assert repos[2] == ('conceptsplitter', 'Extract atomic concepts from a given text using the OpenAI API.')
    assert repos[3] == ('textdownloader', 'A browser extension to automatically generate text dumps for processing.')

def test_main_function_writes_to_files(mocker, tmp_path):
    mocker.patch('noteutilsyncer.fetch_gist_repos.fetch_gist_content', return_value=[
        ('repo1', 'description1'),
        ('repo2', 'description2')
    ])
    repo_file_path = tmp_path / "repos.txt"
    desc_file_path = tmp_path / "descriptions.txt"
    
    from noteutilsyncer.fetch_gist_repos import main
    main(repo_file_path=repo_file_path, description_file_path=desc_file_path)

    # Re-read the repo file after writing to validate its content
    with open(repo_file_path, 'r') as f:
        repo_content = f.read()

    # Re-read the description file after writing to validate its content
    with open(desc_file_path, 'r') as f:
        desc_content = f.read()

    assert repo_content == "repo1\nrepo2\n"
    assert desc_content == "description1\ndescription2\n"
