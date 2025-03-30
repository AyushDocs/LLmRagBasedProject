import json
import os
import requests
from Project.mapper import TOOL_FUNCTION_MAPPER

def solve(question: str,ROOT_DIR:str,file_path:str) -> dict:
    question=question if file_path is None else question+'file is located at '+file_path 
    output = get_output(question,ROOT_DIR)
    return output

def classify_and_call_function(question,tools):
    # OpenAI API endpoint
    url = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    
    # Headers with the API key
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
        "Content-Type": "application/json"
    }
    
    # Request payload
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": question}
        ],
        "tools": tools,
        "tool_choice": "required"
    }
    
    # Send the POST request to OpenAI
    response = requests.post(url, headers=headers, json=payload)
    
    # Parse the response
    if response.status_code == 200:
        result = response.json()
        print(result)
        message = result["choices"][0]["message"]
        
        # Check if a function call was suggested
        if "tool_calls" in message:
            tool_call = message["tool_calls"][0]
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])    
            print(function_name+":"+str(function_args))
            output=TOOL_FUNCTION_MAPPER[function_name](function_args)
            return output        
        
        else:
            print("No function call suggested.")
            print(f"Response: {message['content']}")
    
    else:
        print(f"Error: {response.status_code}")
        print(response.text)


def get_output(question:str,ROOT_DIR:str):
    """
    Reads tools from JSON files in the project directory and returns them as a list of dictionaries.
    """
    tools_json_file_paths = ["ga1.json", "ga2.json", "ga3.json", "ga4.json", "ga5.json"]
    tools = []

    for file_name in tools_json_file_paths:
        file_path = os.path.join(ROOT_DIR, file_name)
        with open(file_path, "r") as file:
            tools.extend(json.load(file))
    return classify_and_call_function(question,tools)


