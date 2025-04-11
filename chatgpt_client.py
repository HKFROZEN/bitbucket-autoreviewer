import openai
import os
import requests
import time
import json
import traceback

openai_admin_api_key = os.getenv('OPENAI_ADMIN_KEY')
openai_api_key = os.getenv('OPENAI_KEY')
g_review_master_dir = "reviews"

FREE_TIER_LIMIT = 0
def check_day_usage():
    url = 'https://api.openai.com/v1/organization/usage/completions'
    day_in_unix = 24 * 60 * 60
    unix_timestamp = str(int(time.time()) - day_in_unix)
    
    params = {
    "start_time": unix_timestamp
    }
    headers={"Authorization": f"Bearer {openai_admin_api_key}",
             "Content-Type":"application/json"
    
    }

    response = requests.get(url, params=params,headers=headers)
    if response.status_code == 200:
        try:
            response_json = response.json()
            num_of_model_requests = 0
            input_tokens = 0
            output_tokens = 0
            for item in response_json['data']:
                for result in item['results']:
                    num_of_model_requests+=result['num_model_requests']
                    input_tokens+=result['input_tokens']
                    output_tokens+=result['output_tokens']
            return (num_of_model_requests,input_tokens,output_tokens)
        except ValueError:
            print("Response is not in valid JSON format.")
        else:
            print(f"Request failed with status code {response.status_code}")
    return False

def review_diff_file(diff_filename):
    ret = None
    url = "https://api.openai.com/v1/chat/completions"
    diff_string =""
    diff_file = open(diff_filename,'r')

    for line in diff_file.readlines():
        diff_string+= line +"\n"


    payload = json.dumps({
        "model": "gpt-4o-mini-2024-07-18",
        "messages": [
      {
        "role": "developer",
        "content": "You are a code reviewer, look at the diff file and make helpful comments that improve readablity and performance. When the user gives you text, assume it to be in a diff format"
      },
      {
        "role": "user",
        "content": diff_string
      }  
        ]
    })

    headers = {"Authorization": f"Bearer {openai_api_key}",
                
             "Content-Type":"application/json"

    }
        
    
    if not os.path.exists(g_review_master_dir):
        os.makedirs(g_review_master_dir)

    review_file = open(f"{g_review_master_dir}/{diff_filename[:-4]}review",'w') #assuming format file.diff

    response = requests.request("POST",url,data=payload,headers=headers)
    if response.status_code == 200:
        try:
            response_json = response.json()
            num_of_model_requests = 0
            input_tokens = 0
            output_tokens = 0
            for choice in response_json['choices']:
                content = choice['message']['content']
                review_file.write(content)
            return 
        except ValueError:
            print("Response is not in valid JSON format.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            traceback.print_exc()
            print(f"Request failed with status code {response.status_code}")
            raise e
    return ret 