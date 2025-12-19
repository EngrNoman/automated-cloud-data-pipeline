import os
import json
import boto3
import pandas as pd  # Pandas import karna zaroori hai type checking k liye
from datetime import datetime
from utils.logger import get_logger

logger = get_logger("STORAGE")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

ENV = os.getenv("ENV_TYPE", "local")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3_client = boto3.client("s3")

def save_data(data, folder, filename_prefix, file_type="json"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # --- 1. Content Preparation (Convert Data to String) ---
    content = ""
    content_type = ""
    filename = ""

    if file_type == "json":
        filename = f"{filename_prefix}_{timestamp}.json"
        # Data ko String banaya
        content = json.dumps(data, indent=4)
        content_type = "application/json"

    elif file_type == "csv":
        filename = f"{filename_prefix}_{timestamp}.csv"
        content_type = "text/csv"
        
        # Check karein k data waqayi DataFrame hai?
        if isinstance(data, pd.DataFrame):
            # IMPORTANT: index=False string return karta hai (File my save nahi karta)
            content = data.to_csv(index=False) 
        else:
            # Agar ghalati se list aa gayi to error na aye
            logger.warning("Data was expected to be DataFrame but got something else. Saving as String.")
            content = str(data)

    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    # --- 2. Saving Logic ---
    
    # LOCAL MODE
    if ENV == "local":
        full_path = os.path.join("data", folder, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Encoding utf-8 zaroori hai
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)  # <--- Ab ye 'content' pakka String hai
        
        return full_path

    # CLOUD MODE
    else:
        if not BUCKET_NAME:
            logger.error("❌ BUCKET_NAME missing in Cloud Mode.")
            raise ValueError("BUCKET_NAME is not set.")

        s3_key = f"{folder}/{filename}"
        
        if ENV != "local":
            logger.info(f"Uploading to S3: {BUCKET_NAME}/{s3_key}")

        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=content,  # AWS ko bhi String chahiye
            ContentType=content_type
        )
        return f"s3://{BUCKET_NAME}/{s3_key}"