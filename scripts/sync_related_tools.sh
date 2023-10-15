#!/bin/bash

# Fetch the Gist content
curl -s https://gist.github.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/ > gist_related_tools.txt

# Extract the "Related Tools" section from current README
sed -n '/<!--START_TAG-->/, /<!--END_TAG-->/p' README.md > current_related_tools.txt

# Compare the Gist content with the current section
if ! diff gist_related_tools.txt current_related_tools.txt; then
    # Update the README
    sed -i '/<!--START_TAG-->/, /<!--END_TAG-->/c\<!--START_TAG-->\n'$(cat gist_related_tools.txt)'\n<!--END_TAG-->' README.md
    git config --global user.name 'GitHub Action'
    git config --global user.email 'action@github.com'
    git add README.md
    git commit -m 'Update Related Tools section from Gist'
    git push

    # Update related repositories' READMEs
    for repo in $(cat gist_related_tools.txt); do
    python scripts/utils.py update_repo_readme $repo
    done


    # Extract repo URLs and update them
    python scripts/utils.py
fi
