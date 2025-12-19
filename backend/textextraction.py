import base64
import requests
from preprocessing import process_image

OLLAMA_URL = "http://localhost:11434/api/generate"

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def text_extraction(imaurl):
    image_b64 = image_to_base64(imaurl)

    payload = {
        "model": "deepseek-ocr",
        "prompt": "Extract all visible text in perfect possible expression appears.",
        "images": [image_b64],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()
    return result['generations'][0]['text']