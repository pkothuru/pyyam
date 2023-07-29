import git
import os

def get_added_lines_in_yaml(repo_path, yaml_file_path):
    repo = git.Repo(repo_path)
    head_commit = repo.head.commit

    diff = repo.git.diff(head_commit.parents[0], head_commit, "--", yaml_file_path)

    added_lines = []
    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line.strip("+ ").strip())

    return added_lines

if __name__ == "__main__":
    repo_path = "/Users/priyatha.kothuru/Desktop/pyyam"  # Replace this with the path to your Git repository
    yaml_file_path = "/Users/priyatha.kothuru/Desktop/pyyam/sample.yaml"  # Replace this with the actual path to your YAML file

    if not os.path.exists(repo_path):
        print(f"Error: Repository path '{repo_path}' does not exist.")
        exit(1)

    if not os.path.exists(yaml_file_path):
        print(f"Error: YAML file '{yaml_file_path}' does not exist.")
        exit(1)

    try:
        added_lines = get_added_lines_in_yaml(repo_path, yaml_file_path)
        if not added_lines:
            print("No newly added lines found in the YAML file between the working directory and the latest commit.")
        else:
            print("Newly added lines in the YAML file between the working directory and the latest commit:")
            for line in added_lines:
                print(line)
                break
    except git.GitCommandError as e:
        print(f"Error: {e}")
