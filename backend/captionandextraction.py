# performing the paralle procssing 
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
def process_image(imgurl):
    with Image.open(imgurl) as img:
        exif_data = img.getexif()
    if not exif_data:
        return "thre is no such date created"
    # making the 

def  processing_parra(imgurl):
    print("####### IMAGE PROCESSING DO ############")
    metadata=process_image(imgurl)
