from github import Github


def get_repo_pr_contents(repo_url, path=''):

    g = Github()
    _, _, repo_owner, repo_name = repo_url.rstrip('/').split('/')[-4:]

    # Get the repository
    repo = g.get_repo(f"{repo_owner}/{repo_name}")

    pull_requests =  repo.get_pulls(state="open", sort="created")
    if pull_requests.totalCount == 0:
        return [],[],"",""
    else :
        pull_request = pull_requests[0]

    # Get the files that have changed in the pull request
    files = pull_request.get_files()
    branch = pull_request.head.ref
    diff_url = pull_request.diff_url
    master_contents = []
    pr_contents = []

    # Iterate over the changed files
    for file in files:
        # Get the file path
        file_path = file.filename

        try: 
            # Get the file contents from the master branch
            master_content = repo.get_contents(file_path, ref="main").decoded_content.decode("utf-8")
            master_contents.append(f"FileName: {file_path} \\n {master_content}")
        except Exception as e:
            print ('main brach not found')

        try: 
            # Get the file contents from the master branch
            master_content = repo.get_contents(file_path, ref="master").decoded_content.decode("utf-8")
            master_contents.append(f"FileName: {file_path} \\n {master_content}")
        except Exception  as e:
            print ('master brach not found')
        

        # Get the file contents from the pull request branch
        pr_content = repo.get_contents(file_path, ref=pull_request.head.ref).decoded_content.decode("utf-8")
        pr_contents.append(f"FileName: {file_path} \\n {pr_content}")

        return master_contents, pr_contents, branch, diff_url



# # Example usage
# repo_link = "https://github.com/Team-Brewmasters/code-compass-webapp"
# file_contents_array = get_repo_file_contents(repo_link)

# # Print the file contents array
# for file_content in file_contents_array:
#     print(file_content)
#     print("---")