import requests
import os
import re
from collections import defaultdict

auth_token = os.getenv('BITBUCKET_TOKEN')
g_pr_master_diff_file = 'pr_master_diff.diff'
def get_pr_text(baseurl,projectKey,repositorySlug,pullRequestId):
    url = f"{baseurl}/rest/api/latest/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}"

    headers = {
    "Accept": "application/json;charset=UTF-8",
    'Authorization': f'Bearer {auth_token}' 
    }

    response = requests.request(
    "GET",
    url,
    headers=headers
    )

def split_patch_by_file():
    file_patches = defaultdict(list)
    with open(g_pr_master_diff_file, "r", encoding="utf-8") as f:
        line = f.readline()
        current_file = None
        while line is not None and line!='':
            if re.search(r"diff --git src://.*dst://" ,line):
                current_file = re.search(r"src://.* ",line).group().strip()[len('src://'):]
            file_patches[current_file].append(line)
            line = f.readline()
        
        
    for file_name, patch_lines in file_patches.items():
        output_file = file_name.replace("/", "_") + ".diff"
        with open(output_file, "w", encoding="utf-8") as f:
            f.writelines(patch_lines)
        print(f"Saved patch for {file_name} to {output_file}")
    

def get_pr_diff(baseurl,projectKey,repositorySlug,pullRequestId):
    url = f"{baseurl}/rest/api/latest/projects/{projectKey}/repos/{repositorySlug}/pull-requests/{pullRequestId}.diff"

    headers = {
    'Authorization': f'Bearer {auth_token}' 
    }

    response = requests.request(
    "GET",
    url,
    headers=headers
    )

    response.text
    file = open(g_pr_master_diff_file,'w')
    file.write(response.text)
    file.close()