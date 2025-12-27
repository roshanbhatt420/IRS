import os
from datetime import datetime
from PIL import Image
# import easyocr  <-- REMOVED (Not used)
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from sentence_transformers import SentenceTransformer
import chromadb
import base64
import requests
import concurrent.futures

print("Loading AI Models...")

# ollama setup
OLLAMA_URL = "http://localhost:11434/api/generate"

OLLAMA_MODEL = "deepseek-ocr" 

# 1loading blip model
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# load sentence transformer for embeddings
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# loaidnf data base
client = chromadb.PersistentClient(path="./brain_db")
collection = client.get_or_create_collection(name="screenshots")


def image_to_base64(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_

    """
    if not os.path.exists(path):
        raise FileNotFoundError("No such file ")
    try:
        with open(path, "rb") as f:
            encoded= base64.b64encode(f.read()).decode("utf-8")
            return encoded
    except Exception  as e:
        raise  RuntimeError(f"Error in encoding {e}")

def process_image(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Metadata
    stats = os.stat(file_path)
    creation_time = datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d')
    
    # Image Load & Resize
    image = Image.open(file_path).convert("RGB")
    if image.width > 1000:
        ratio = 1000 / image.width
        new_height = int(image.height * ratio)
        image = image.resize((1000, new_height))
        
    return image, {"date": creation_time, "path": file_path}


def extract_text_ollama(image_path):
    """
    Extracts text and structure from an image using Ollama.
    """
    image_b64 = image_to_base64(image_path)
    print("Sending image to Ollama for OCR...")

    prompt = (
    "Descibes the image "    )
    payload={
        "model":OLLAMA_MODEL,
        "prompt":prompt,
        "images": [image_b64],
        "stream": False,
                  }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
        )
        response.raise_for_status()
        print("Ollama response received.")



        data = response.json()
        return data.get("response", "[No OCR text returned]")

    except Exception as e:
        print(f"Ollama Error: {e}")
        
        return "[Ollama Failed to Read Text]"


def generate_caption(image):
    """_summary_

    Args:
        image (_type_): _description_

    Returns:
        _type_: _description_
    """
    inputs = processor(image, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

def ingest_screenshot(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    print(f"Processing: {file_path}...")
    image, metadata = process_image(file_path)
    ocr_text = ""
    caption = ""
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        
        future_ocr = executor.submit(extract_text_ollama, file_path)
        
        
        future_caption = executor.submit(generate_caption, image)
        
        ocr_text = future_ocr.result()
        caption = future_caption.result()
    
 
    context = f"Visual Summary: {caption}.\nDetailed Content: {ocr_text}"

    vector = embedder.encode(context).tolist()

    collection.add(
        ids=[file_path],
        embeddings=[vector],
        metadatas=[metadata],
        documents=[context]
    )
    print("Saved to Brain!")
    return context

def search_brain(query_text, date_filter=None):
    """_summary_

    Args:
        query_text (_type_): _description_
        date_filter (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    print(f"Searching for: {query_text}")
    query_vector = embedder.encode(query_text).tolist()
    
    where_clause = None
    if date_filter:
        where_clause = {"date": date_filter}

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=3,
        where=where_clause
    )
    
    return results

if __name__ == "__main__":
    # Example usage
    test_image_path = "../datasets/1.png"  # Replace with your test image path
    print(ingest_screenshot(test_image_path))
    
   