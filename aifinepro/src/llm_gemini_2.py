import os
import json
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.utils import parse_json_from_llm_response
load_dotenv()
client_1 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_1"])
client_2 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_2"])
client_3 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_3"])
client_4 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_4"])
client_5 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_5"])

# Dictionary để map index với client
clients_map = {
    1: client_1,
    2: client_2,
    3: client_3,
    4: client_4,
    5: client_5
}
def llm_vision(prompt):
    """
    Function to invoke the LLM with vision capabilities.
    """
    try:
        # Example of invoking a model with vision capabilities
        # Replace with your actual model and parameters
        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "qwen/qwen2.5-vl-72b-instruct",
            "messages": prompt,
            'provider': {
                'order': [
                    'phala'
                ]
                }
        })
        )
        return response.json()
    except Exception as e:
        raise Exception(f"Error invoking LLM: {str(e)}")

def llm_gemini(list_path, prompt):

    images = []
    for path in list_path:
        with open(path, 'rb') as f:
            img_bytes = f.read()
            image_type = types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/png'
            )
            images.append(image_type)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                *images
            ],
        ),
    ]
    config_params = {
        "temperature": 0.5,
        "thinking_config": types.ThinkingConfig(thinking_budget=-1),
    }

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    response = client_2.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )
    result = parse_json_from_llm_response(response.text)
    return result

def llm_gemini_flex(list_path, index, prompt):
    """
    Flexible LLM function that uses different clients based on index
    
    Args:
        list_path: List of image paths
        index: Client index (1-5)
        prompt: Text prompt
    
    Returns:
        Parsed JSON response
    """
    # Chọn client dựa trên index
    selected_client = clients_map.get(index, client_2)  # Default to client_2 if index not found
    
    print(f"Using client_{index} for this request")
    
    images = []
    for path in list_path:
        with open(path, 'rb') as f:
            img_bytes = f.read()
            image_type = types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/png'
            )
            images.append(image_type)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                *images
            ],
        ),
    ]
    config_params = {
        "temperature": 0.5,
        "thinking_config": types.ThinkingConfig(thinking_budget=-1),
    }

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    try:
        response = selected_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=generate_content_config,
        )
        result = parse_json_from_llm_response(response.text)
        return result
    except Exception as e:
        print(f"Error with client_{index}: {str(e)}")
        raise Exception(f"Error invoking LLM with client_{index}: {str(e)}")
    
def llm_gemini_flex_no_thinkhing(list_path, index, prompt):
    """
    Flexible LLM function that uses different clients based on index
    
    Args:
        list_path: List of image paths
        index: Client index (1-5)
        prompt: Text prompt
    
    Returns:
        Parsed JSON response
    """
    # Chọn client dựa trên index
    selected_client = clients_map.get(index, client_2)  # Default to client_2 if index not found
    
    print(f"Using client_{index} for this request")
    
    images = []
    for path in list_path:
        with open(path, 'rb') as f:
            img_bytes = f.read()
            image_type = types.Part.from_bytes(
                data=img_bytes,
                mime_type='image/png'
            )
            images.append(image_type)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                *images
            ],
        ),
    ]
    config_params = {
        "temperature": 0.5,
        "thinking_config": types.ThinkingConfig(thinking_budget=0),
    }

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    try:
        response = selected_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=generate_content_config,
        )
        result = parse_json_from_llm_response(response.text)
        return result
    except Exception as e:
        print(f"Error with client_{index}: {str(e)}")
        raise Exception(f"Error invoking LLM with client_{index}: {str(e)}")