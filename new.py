import git
import os

def get_added_names_in_yaml(repo_path, yaml_file_path):
    repo = git.Repo(repo_path)
    head_commit = repo.head.commit

    diff = repo.git.diff(head_commit.parents[0], head_commit, "--", yaml_file_path)

    added_names = []
    in_added_block = False

    for line in diff.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            stripped_line = line.strip("+ ").strip()
            if stripped_line.startswith("name: "):
                added_names.append(stripped_line.split(": ", 1)[1])

    return added_names

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
        added_names = get_added_names_in_yaml(repo_path, yaml_file_path)
        if not added_names:
            print("No newly added 'name' fields found in the YAML file between the working directory and the latest commit.")
        else:
            print("Newly added 'name' fields in the YAML file between the working directory and the latest commit:")
            for name in added_names:
                print(name)
    except git.GitCommandError as e:
        print(f"Error: {e}")
