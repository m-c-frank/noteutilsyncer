#!/bin/bash

# Directory containing all READMEs
READMES_DIR="READMEs"

# Extract the "Related Tools" section from a given README
extract_related_tools_section() {
    local readme=$1
    sed -n '/^## Related Tools$/,/^##/p' $readme
}

# Update the README in the given repository
update_repository() {
    local repo=$1
    local related_tools_section="$2"
    local repo_name=$(basename $repo .git)
    local branch_name="update-related-tools"

    # Clone the repository
    git clone $repo

    # Create a new branch
    cd $repo_name
    git checkout -b $branch_name

    # Replace the "Related Tools" section
    sed -i "/^## Related Tools$/,/^##/c$related_tools_section" README.md

    # Commit and push changes
    git add README.md
    git commit -m "Update Related Tools section"
    git push origin $branch_name

    # Authenticate GitHub CLI and create a pull request
    echo $GH_PAT | gh auth login --with-token
    gh pr create --base main --head $branch_name --title "Update Related Tools section" --body "Automated update of the Related Tools section."

    cd ..
}

main() {
    # Extract the "Related Tools" section from each README
    for readme in $READMES_DIR/*.md; do
        local related_tools_section=$(extract_related_tools_section $readme)
        local repo_url=$(grep -oP 'https://github.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+(?=\))' $readme | head -1)

        # Update the corresponding repository
        update_repository $repo_url "$related_tools_section"
    done
}

main
