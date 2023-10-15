import pytest
import os
from src.sync import extract_related_tools_section, update_repository

# Parameterized test for extract_related_tools_section
@pytest.mark.parametrize("content, expected_section", [
    ("""
    # Project Title

    ## Features
    - Feature A
    - Feature B

    ## Related Tools
    - Tool A
    - Tool B

    ## License
    MIT License
    """, 
    "## Related Tools\n\n- Tool A\n- Tool B"
    ),
    # Add more test cases as needed
])
def test_extract_related_tools_section(content, expected_section):
    with open("mock_readme.md", "w") as f:
        f.write(content)

    section = extract_related_tools_section("mock_readme.md")
    assert section == expected_section

    os.remove("mock_readme.md")

# Mock the subprocess.run function to avoid actual git operations
@pytest.fixture
def mock_subprocess(mocker):
    mocker.patch("subprocess.run")

def test_update_repository(mock_subprocess):
    # Mock a README content
    content = """
    # Project Title

    ## Features
    - Feature A
    - Feature B

    ## Related Tools
    - Tool A
    - Tool B

    ## License
    MIT License
    """
    with open("mock_readme.md", "w") as f:
        f.write(content)

    related_tools_section = extract_related_tools_section("mock_readme.md")
    update_repository("mock_repo", related_tools_section, "mock_token")

    # Additional assertions can be added based on the expected behavior of the update_repository function

    os.remove("mock_readme.md")

# Test for Missing "Related Tools" Section
@pytest.mark.parametrize("content", [
    """
    # Project Title

    ## Features
    - Feature A
    - Feature B

    ## License
    MIT License
    """
])
def test_extract_related_tools_section_missing_section(content):
    with open("mock_readme.md", "w") as f:
        f.write(content)

    with pytest.raises(ValueError, match="Missing 'Related Tools' section"):
        extract_related_tools_section("mock_readme.md")

    os.remove("mock_readme.md")

# Test for Empty "Related Tools" Section
@pytest.mark.parametrize("content", [
    """
    # Project Title

    ## Features
    - Feature A
    - Feature B

    ## Related Tools

    ## License
    MIT License
    """
])
def test_extract_related_tools_section_empty_section(content):
    with open("mock_readme.md", "w") as f:
        f.write(content)

    section = extract_related_tools_section("mock_readme.md")
    assert section == "## Related Tools"

    os.remove("mock_readme.md")
