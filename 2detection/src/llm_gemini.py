import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from google import genai
from google.genai import types
from PIL import Image
from src.info_image import read_image

load_dotenv()
client_llm3 = genai.Client(api_key=os.environ["GOOGLE_API_KEY_LLM3"])
client_llm = genai.Client(api_key=os.environ["GOOGLE_API_KEY_LLM"])

safety_settings = [
    types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="BLOCK_ONLY_HIGH",
    ),
]

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5,
    safety_settings={
        3: 2  # 3 = Dangerous Content, 2 = BLOCK_ONLY_HIGH
    },
    model_kwargs={
        "thinking_config": {"thinking_budget": -1}
    },
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

llm_2 = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1
)

def llm_3_invoke(image_url, prompt, width, height, image):
    target_height = int(1024 * height / width)
    resized_image = image.resize((1024, target_height), Image.Resampling.LANCZOS)

    response = client_llm3.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, resized_image],
        config = types.GenerateContentConfig(
            temperature=0.5,
            safety_settings=safety_settings,
            thinking_config=types.ThinkingConfig(
            thinking_budget= 0# Set thinking budget to 30 seconds
            )
        )
    )
    return response.text

def llm_3_invoke_multi(image_urls, prompt):
    """
    Truyền vào một list image_urls và prompt, gửi tất cả ảnh cùng lúc cho Gemini.
    """
    images = []
    for image_url in image_urls:
        _, height, image = read_image(image_url)
        width = image.width
        target_height = int(1024 * height / width)
        resized_image = image.resize((1024, target_height), Image.Resampling.LANCZOS)
        images.append(resized_image)

    contents = [prompt] + images

    response = client_llm.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            temperature=0.5,
            safety_settings=safety_settings,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            )
        )
    )
    return response.text