import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"

def fetch_gist_content():
    response = requests.get(GIST_URL)
    response.raise_for_status()
    lines = response.text.strip().split('\n')
    repos = []
    for line in lines:
        repo, description = line.split(",", 1)
        repos.append((repo.strip("'"), description.strip("'")))
    return repos

def main():
    repos = fetch_gist_content()
    with open("repos.txt", "w") as f:
        for repo, _ in repos:
            f.write(f"{repo}\n")

if __name__ == "__main__":
    main()