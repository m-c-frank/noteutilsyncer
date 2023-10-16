import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"


def fetch_gist_content():
    response = requests.get(GIST_URL)
    response.raise_for_status()
    lines = response.text.strip().split('\n')
    repos = []
    for line in lines:
        repo, description = line.split(",", 1)
        repo, description = repo.strip("'"), description.strip("'")
        print(f"Processed: Repo - {repo}, Description - {description}")
        repos.append((repo, description))
    return repos

def main():
    print("Fetching gist content...")
    repos = fetch_gist_content()
    with open("repos.txt", "w") as f:
        for repo, _ in repos:
            f.write(f"{repo}\n")

if __name__ == "__main__":
    main()