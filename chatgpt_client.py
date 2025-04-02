import openai
import os
import requests
import time
openai_api_key = os.getenv('OPENAI_KEY')

FREE_TIER_LIMIT = 0
def check_day_usage():
    url = 'https://api.openai.com/v1/organization/usage/completions'
    day_in_unix = 24 * 60 * 60
    unix_timestamp = str(int(time.time()) - day_in_unix)
    
    params = {
    "start_time": unix_timestamp
    }
    headers={"Authorization": f"Bearer {openai_api_key}",
             "Content-Type":"application/json"
    
    }

    response = requests.get(url, params=params,headers=headers)
    if response.status_code == 200:
        try:
            # Convert the response content to a JSON dictionary
            response_json = response.json()
            print("Response as JSON:", response_json)
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