import requests

GIST_URL = "https://gist.githubusercontent.com/m-c-frank/5b7a099c0998e3030888125370b26195/raw/"


def fetch_gist_content():
    response = requests.get(GIST_URL)
    response.raise_for_status()
    lines = response.text.strip().split('\n')
    repos = []
    for line in lines:
        # Splitting based on the first comma
        parts = line.split(',', 1)
        repo = parts[0].strip("'").strip()
        description = parts[1].strip("'").strip() if len(parts) > 1 else ""
        print(f"Processed: Repo - {repo}, Description - {description}")
        repos.append((repo, description))
    return repos


def main(repo_file_path="repos.txt", description_file_path="descriptions.txt"):
    print("Fetching gist content...")
    repos = fetch_gist_content()
    with open(repo_file_path, "w") as repo_file, open(description_file_path, "w") as desc_file:
        for repo, description in repos:
            repo_file.write(f"{repo}\n")
            desc_file.write(f"{description}\n")

if __name__ == "__main__":
    main()