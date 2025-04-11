import os
import requests
import bitbucket_client
import chatgpt_client


def lambda_handler(event, context):
    ret = True   
    base_url = event['base_url']
    project_key = event['proj_key']
    repo_slug = event['repo']
    pr_id = event['pr_id']
    
    bitbucket_client.get_pr_text(base_url,project_key,repo_slug,pr_id)
    bitbucket_client.get_pr_diff(base_url,project_key,repo_slug,pr_id)
    diff_files = bitbucket_client.split_patch_by_file()
    for diff_file in diff_files:
        print(chatgpt_client.check_day_usage())
        chatgpt_client.review_diff_file(diff_file)
    return ret

event = {'base_url' : os.getenv('BASE_URL'),
'proj_key' : os.getenv('PROJECT_KEY'),
'repo' : os.getenv('REPO_SLUG'),
'pr_id' : os.getenv('PR_ID'),
'open_ai_key':os.getenv('OPENAI_KEY')}

lambda_handler(event,{})