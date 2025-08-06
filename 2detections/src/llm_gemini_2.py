from google import genai
from google.genai import types
import os
import requests
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
client_2 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_LLM3"])

def llm_gemini_nothinking(list_urls, prompt, prompt_system=None):

    images = []
    for url in list_urls:
        image_bytes = requests.get(url).content
        image = types.Part.from_bytes(
            data=image_bytes, mime_type="image/jpeg"
        )
        images.append(image)

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

    if prompt_system:
        config_params["system_instruction"] = [
            types.Part.from_text(text=prompt_system),
        ]

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )
    return response.text

def llm_gemini_thinking(list_urls, prompt, prompt_system=None):

    print(list_urls)
    images = []
    for url in list_urls:
        image_bytes = requests.get(url).content
        image = types.Part.from_bytes(
            data=image_bytes, mime_type="image/jpeg"
        )
        images.append(image)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                *images
            ],
        ),
    ]
    print(contents)


    config_params = {
        "temperature": 0.5,
        "thinking_config": types.ThinkingConfig(thinking_budget=-1),
    }

    if prompt_system:
        config_params["system_instruction"] = [
            types.Part.from_text(text=prompt_system),
        ]

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )
    return response.text

def llm_gemini_thinking_2(list_urls, prompt, prompt_system=None):

    print(list_urls)
    images = []
    for url in list_urls:
        image_bytes = requests.get(url).content
        image = types.Part.from_bytes(
            data=image_bytes, mime_type="image/jpeg"
        )
        images.append(image)

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
                *images
            ],
        ),
    ]
    print(contents)


    config_params = {
        "temperature": 0.5,
        "thinking_config": types.ThinkingConfig(thinking_budget=-1),
    }

    if prompt_system:
        config_params["system_instruction"] = [
            types.Part.from_text(text=prompt_system),
        ]

    generate_content_config = types.GenerateContentConfig(**config_params)

    print(generate_content_config)

    response = client_2.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    )
    return response.text

