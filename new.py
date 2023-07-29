import git
import os
import yaml

def get_yaml_changes(repo_path, yaml_file_path):
    repo = git.Repo(repo_path)
    commits = list(repo.iter_commits(max_count=2))

    if len(commits) < 2:
        print("Error: Not enough commits in the repository.")
        return None

    commit1 = commits[1]
    commit2 = commits[0]

    diff = repo.git.diff(commit1, commit2, "--name-only")
    changed_files = diff.splitlines()

    if yaml_file_path in changed_files:
        yaml_changes = repo.git.diff(commit1, commit2, "--", yaml_file_path)
        return yaml_changes
    else:
        return None

def load_yaml_file(file_path):
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    repo_path = "/Users/priyatha.kothuru/Desktop/pyyam"  # Replace this with the path to your Git repository
    yaml_file_path = "/Users/priyatha.kothuru/Desktop/pyyam/sample.yaml"  # Replace this with the actual path to your YAML file

    if not os.path.exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist.")
        exit(1)

    if not os.path.exists(yaml_file_path):
        print(f"Error: YAML file '{yaml_file_path}' does not exist.")
        exit(1)

    yaml_changes = get_yaml_changes(repo_path, yaml_file_path)
    if yaml_changes is None:
        print("No differences found in the 'name' field of the YAML file between the last two commits.")
    else:
        print("Changes in the YAML file between the last two commits:")
        print(yaml_changes)

        # Extract and print the names of the differences from the Git diff
        names_of_differences = []
        for line in yaml_changes.splitlines():
            if line.strip().startswith("- name: "):
                name = line.strip().split(": ")[1]
                names_of_differences.append(name)

        print("Names of the differences:")
        print(names_of_differences)

        # Optionally, you can also load and print the YAML content for the latest commit:
        latest_yaml_content = load_yaml_file(yaml_file_path)
        print("Latest YAML content:")
        print(yaml.dump(latest_yaml_content, default_flow_style=False))
