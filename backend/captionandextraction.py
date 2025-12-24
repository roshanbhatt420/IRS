# performing the paralle procssing 
from PIL import Image
import os
from PIL.ExifTags import TAGS
from datetime import datetime
import concurrent.futures

from textextraction import ocr_image 
from captioning import caption_image

def process_image(file_path):
    """
    1. Loads image
    2. Extracts Metadata (Date)
    3. Resizes if too big (Optimization)
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

def  processing_parra(imgurl):
    print("####### IMAGE PROCESSING DO ############")
    image,metadata=process_image(imgurl)
    print("metadata:",metadata)
    print("Image Size:",image.size)
    print(f"Processing Image at {imgurl}")
    ocr_text=""
    caption_text=""
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # working on parallel process 

        future_ocr=executor.submit(ocr_image, imgurl)
        future_caption=executor.submit(caption_image,imgurl)
        # wait for result come
        text_ocr=future_ocr.result()
        text_caption=future_caption.result()
         # Combine results
        context = f"Visual Description: {text_caption}. Text Content: {text_ocr}"

        return context


if __name__=="__main__":
    imgurl="../datasets/1.png"
    print(processing_parra(imgurl))
    


