#!/bin/bash

# Fetch the Gist content
curl -s https://gist.github.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/ > gist_related_tools.txt

# Extract the "Related Tools" section from current README
sed -n '/<!--START_TAG-->/, /<!--END_TAG-->/p' README.md > current_related_tools.txt

# Compare the Gist content with the current section
if ! diff gist_related_tools.txt current_related_tools.txt; then
  # Update the README of main repository
  sed -i '/<!--START_TAG-->/, /<!--END_TAG-->/c\<!--START_TAG-->\n'$(cat gist_related_tools.txt)'\n<!--END_TAG-->' README.md
  git config --global user.name 'GitHub Action'
  git config --global user.email 'action@github.com'
  git add README.md
  git commit -m 'Update Related Tools section from Gist'
  git push https://${GH_PAT}@github.com/m-c-frank/noteutilsyncer.git
  
  # Loop through each related tool and update its README
  while IFS= read -r repo_name; do
    git clone "https://github.com/m-c-frank/${repo_name}.git"
    cd "${repo_name}"
    sed -i '/<!--START_TAG-->/, /<!--END_TAG-->/c\<!--START_TAG-->\n'$(cat ../gist_related_tools.txt)'\n<!--END_TAG-->' README.md
    git add README.md
    git commit -m 'Update Related Tools section from Gist'
    git push https://${GH_PAT}@github.com/m-c-frank/${repo_name}.git
    cd ..
    rm -rf "${repo_name}"  # Cleanup
  done < gist_related_tools.txt
fi
