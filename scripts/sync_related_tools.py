import os
import subprocess
from utils import check_and_update_readme, fetch_gist_content, split_gist_into_repos

def main():
    # Check and update the main README if necessary
    if check_and_update_readme():
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action"])
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"])
        subprocess.run(["git", "add", "README.md"])
        subprocess.run(["git", "commit", "-m", 'Update Related Tools section from Gist'])
        subprocess.run(["git", "push", "origin", "main", "--force", "--quiet", "https://${{GH_PAT}}@github.com/m-c-frank/noteutilsyncer.git"])

    # Fetch the list of repo names from the Gist
    repo_names = split_gist_into_repos(fetch_gist_content())

    # Loop through each repo and update its README
    for repo in repo_names:
        if repo != "noteutilsyncer":
            subprocess.run(["git", "clone", f"https://github.com/m-c-frank/{repo}.git"])
            os.chdir(repo)

            if check_and_update_readme():
                subprocess.run(["git", "add", "README.md"])
                subprocess.run(["git", "commit", "-m", 'Update Related Tools section from central Gist'])
                subprocess.run(["git", "push", "origin", "main", "--force", "--quiet", f"https://${{GH_PAT}}@github.com/m-c-frank/{repo}.git"])

            os.chdir("..")

if __name__ == "__main__":
    main()
