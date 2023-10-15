import os
import subprocess
import utils

def main():
    # Check and update the main repo's README
    if utils.check_and_update_readme():
        # Commit and push changes to the main repo
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Action"])
        subprocess.run(["git", "config", "--global", "user.email", "action@github.com"])
        subprocess.run(["git", "add", "README.md"])
        subprocess.run(["git", "commit", "-m", "Update Related Tools section from Gist"])
        subprocess.run(["git", "push", "origin", "main", "--force", "--quiet", f"https://{os.environ['GH_PAT']}@github.com/m-c-frank/noteutilsyncer.git"])

        # Fetch the updated list of repos from the gist
        repo_names = utils.split_gist_into_repos(utils.fetch_gist_content())

        for repo in repo_names:
            # Clone the repo
            subprocess.run(["git", "clone", f"https://github.com/m-c-frank/{repo}.git"])
            
            # Change directory to the cloned repo
            os.chdir(repo)

            # Update the README
            utils.check_and_update_readme()

            # Commit and push changes
            subprocess.run(["git", "add", "README.md"])
            subprocess.run(["git", "commit", "-m", "Update Related Tools section from Gist"])
            subprocess.run(["git", "push", "origin", "main", "--force", "--quiet", f"https://{os.environ['GH_PAT']}@github.com/m-c-frank/{repo}.git"])

            # Change directory back to the main directory
            os.chdir("..")

if __name__ == "__main__":
    main()
