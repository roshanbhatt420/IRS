import requests
import base64

OLLAMA_URL = "http://localhost:11434/api/generate"

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_text_ocr(image_path):
    image_b64 = image_to_base64(image_path)

    payload = {
        "model": "deepseek-ocr",
        "prompt": (
            "You are a high-precision OCR engine.\n"
            "Descibe the image with all possible visuals details.\n"
            "Describe the scene, objects, text, colors, and layout, whether it is bill, report , screenshots, code error meme etc.\n"
            "Extract all readable text exactly as shown.\n"
            "Do NOT guess or correct text.\n"
            "Preserve formatting, line order, numbers, and symbols.\n"
            "If text is unclear, write [UNCLEAR].\n"
            "Return plain text only."
        ),
        "images": [image_b64],
        "stream": False
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()

    return response.json()["response"]

if __name__ == "__main__":
    image_path = "../datasets/1.png"
    text = extract_text_ocr(image_path)
    print("OCR RESULT:\n")
    print(text)
