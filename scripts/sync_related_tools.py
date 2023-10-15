import os
import subprocess
import utils

def main():
    if utils.check_and_update_readme():
        repo_names = utils.split_gist_into_repos(utils.fetch_gist_content())
        for repo in repo_names:
            if repo == "noteutilsyncer":
                continue  # skip the current repository

            # Clone the repo
            subprocess.run(["git", "clone", f"https://github.com/m-c-frank/{repo}.git"])
            
            # Modify its README
            with open(f"{repo}/README.md", 'r') as f:
                content = f.read()
            new_section = utils.create_related_tools_section(repo_names)
            updated_content = utils.replace_section_in_content(content, new_section)
            with open(f"{repo}/README.md", 'w') as f:
                f.write(updated_content)
            
            # Commit the changes
            subprocess.run(["git", "-C", repo, "add", "README.md"])
            subprocess.run(["git", "-C", repo, "commit", "-m", "Update Related Tools section from noteutilsyncer"])

if __name__ == "__main__":
    main()
