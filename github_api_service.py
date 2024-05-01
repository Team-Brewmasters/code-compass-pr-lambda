import base64

import requests


def get_repo_pr_contents(repo_url, path=''):
    _, _, repo_owner, repo_name = repo_url.rstrip('/').split('/')[-4:]

    # Get the list of pull requests
    pulls_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    pulls_params = {
        "state": "open",
        "sort": "created",
        "direction": "desc"
    }
    pulls_response = requests.get(pulls_url, params=pulls_params)
    pulls_data = pulls_response.json()

    if len(pulls_data) == 0:
        return [], [], "", ""
    else:
        pull_request = pulls_data[0]
        pr_number = pull_request["number"]

        # Get the files that have changed in the pull request
        files_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files"
        files_response = requests.get(files_url)
        files_data = files_response.json()

        branch = pull_request["head"]["ref"]
        diff_url = pull_request["diff_url"]

        master_contents = []
        pr_contents = []

        # Iterate over the changed files
        for file_data in files_data:
            file_path = file_data["filename"]

            try:
                # Get the file contents from the main branch
                master_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
                master_params = {
                    "ref": "main"
                }
                master_response = requests.get(master_url, params=master_params)

                if master_response.status_code == 200:
                    master_content = master_response.json()["content"]
                    master_content = base64.b64decode(master_content).decode("utf-8")
                    master_contents.append(f"FileName: {file_path} \n {master_content}")
            except Exception as e:
                print('Main branch not found')

            try:
                # Get the file contents from the master branch
                master_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
                master_params = {
                    "ref": "master"
                }
                master_response = requests.get(master_url, params=master_params)

                if master_response.status_code == 200:
                    master_content = master_response.json()["content"]
                    master_content = base64.b64decode(master_content).decode("utf-8")
                    master_contents.append(f"FileName: {file_path} \n {master_content}")
            except Exception as e:
                print('Master branch not found')

            # Get the file contents from the pull request branch
            pr_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{file_path}"
            pr_params = {
                "ref": branch
            }
            pr_response = requests.get(pr_url, params=pr_params)

            if pr_response.status_code == 200:
                pr_content = pr_response.json()["content"]
                pr_content = base64.b64decode(pr_content).decode("utf-8")
                pr_contents.append(f"FileName: {file_path} \n {pr_content}")
            else:
                print(f"File not found in pull request branch: {file_path}")

        return master_contents, pr_contents, branch, diff_url