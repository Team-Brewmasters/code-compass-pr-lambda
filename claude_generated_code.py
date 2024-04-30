from github import Github

# Replace with your GitHub access token
access_token = "YOUR_ACCESS_TOKEN"

# Create a GitHub instance
g = Github(access_token)

# Replace with the repository name and owner
repo_name = "REPOSITORY_NAME"
repo_owner = "REPOSITORY_OWNER"

# Get the repository
repo = g.get_repo(f"{repo_owner}/{repo_name}")

# Get the first pull request
pull_request = repo.get_pulls(state="open", sort="created", base="master")[0]

# Get the files that have changed in the pull request
files = pull_request.get_files()

# Iterate over the changed files
for file in files:
    # Get the file path
    file_path = file.filename

    # Get the file contents from the master branch
    master_contents = repo.get_contents(file_path, ref="master").decoded_content.decode("utf-8")

    # Get the file contents from the pull request branch
    pr_contents = repo.get_contents(file_path, ref=pull_request.head.ref).decoded_content.decode("utf-8")

    # Split the contents into arrays of strings
    master_lines = master_contents.split("\n")
    pr_lines = pr_contents.split("\n")

    # Print the file path and the arrays of strings
    print(f"File: {file_path}")
    print("Master contents:")
    print(master_lines)
    print("Pull request contents:")
    print(pr_lines)
    print("---")