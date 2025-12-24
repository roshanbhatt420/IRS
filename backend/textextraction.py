import base64
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    


def ocr_image(image_path):
    image_b64 = image_to_base64(image_path)

    payload = {
        "model": "deepseek-ocr",
        "prompt": """
                    You are a high-precision OCR engine.
                    Extract all readable text exactly as shown.
                    Do NOT guess or correct text.
                    Preserve formatting, line order, numbers, and symbols.
                    If text is unclear, write [UNCLEAR].
                    Return plain text only.
                    and describe the image also .
                    """,
        "images": [image_b64],
        "stream": False
    }

    return requests.post(OLLAMA_URL, json=payload).json()["response"]

if __name__=="__main__":
    test_image_path = "../datasets/1.png"
    ocr_result = ocr_image(test_image_path)
    print("OCR Result:", ocr_result)