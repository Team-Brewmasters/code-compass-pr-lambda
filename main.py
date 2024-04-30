import json

from github_api_service import get_repo_pr_contents
from open_ai_service import call_chatgpt


def lambda_handler(event, context):
    try:
        github_url = event['queryStringParameters']['githubURL']
       
        master_content, pr_content, branch, diff_url = get_repo_pr_contents(github_url)
        if len(pr_content) == 0:
            open_ai_response = {}
        else :
            open_ai_response = call_chatgpt(master_content, pr_content)
            open_ai_response.branch = branch
            open_ai_response.diff_url = diff_url
        
        return {
            'statusCode': 200,
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
            'body': json.dumps(open_ai_response)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e),
            'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
                },
        }
    
# event = {
#     "queryStringParameters":{
#         "githubURL": "https://www.github.com/Team-Brewmasters/code-compass-summary-lambda"
#     }
# }

# res = lambda_handler(event, None)
# print(res)