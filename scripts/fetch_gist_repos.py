import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"

def fetch_gist_content():
    response = requests.get(GIST_URL)
    response.raise_for_status()
    return response.text.strip().split('\n')

def main():
    repo_names = fetch_gist_content()
    
    # Excluding the current repository from the list
    if "noteutilsyncer" in repo_names:
        repo_names.remove("noteutilsyncer")

    # Write the repo names to repos.txt
    with open("repos.txt", "w") as f:
        for repo in repo_names:
            f.write(f"{repo}\n")

if __name__ == "__main__":
    main()
