import requests
import os 
from datetime import datetime
from utils.logger import get_logger

# Logger Setup
logger = get_logger("EXTRACTION_MODULE", "product_api")

# API URL environment variable se lo (Terraform ne set kia hua hai)
API_URL = os.getenv("API_URL", "https://dummyjson.com/products")

def extract_product_data():
    logger.info("--- Pipeline Process Started ---")
    
    if not API_URL:
        logger.error("API_URL missing in environment variables")
        return None

    try:
        logger.info(f"Hitting API: {API_URL}")
        start = datetime.now()
        
        # API Call
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()  # 404/500 errors ko pakro
        
        data = response.json()
        
        duration = datetime.now() - start
        logger.info(f"API Success! Time taken: {duration}. Records fetched: {len(data.get('products', []))}")
        
        # --- ZAROORI: Sirf Data Return karo ---
        # (Save karne ka kaam ab Main Pipeline karega)
        return data
        
    except Exception as e:
        logger.critical(f"API Extraction Failed: {e}")
        return None

if __name__ == "__main__":
    # Local testing k liye print kar k dekh lo
    print(extract_product_data())