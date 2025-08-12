import os
import json
import requests
from google import genai
from google.genai import types
from dotenv import load_dotenv
from src.utils import parse_json_from_llm_response
load_dotenv()
client_2 = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
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