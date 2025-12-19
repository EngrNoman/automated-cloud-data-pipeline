import sys
import os
import json
from datetime import datetime   
from utils.logger import get_logger


# Hum apne extraction module se function import kar rahy hain
from src.ingestion.product_api import extract_product_data
from src.transformation.validator import validate_product_dataset
from src.transformation.transformation import process_validated_data
from src.load.load_data import save_data


try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass #



# Logger setup for Main
logger = get_logger("MAIN_PIPELINE" , "main_pipeline")

def run_pipeline(event=None, context=None):
    logger.info(" --- Pipeline Started ---")
    
    try:
        # ----------------------------------------
        # STEP 1: EXTRACTION (Raw Layer)
        # ----------------------------------------
        logger.info("Extracting Data...")
        raw_data = extract_product_data()

        if not raw_data:
            logger.critical("No data extracted. Exiting pipeline.")
            return
        
        raw_path = save_data(raw_data, "raw", "products_raw", "json")
        logger.info(f" Raw Data Saved at: {raw_path}")
        # ----------------------------------------
        # STEP 2: VALIDATION (Quality Check)
        # ----------------------------------------
        logger.info("Step 2: Validating Data...")
        products_list = raw_data.get('products', [])

        valid_records, invalid_records = validate_product_dataset(products_list)
        logger.info(f"  Validation: Passed={len(valid_records)} | Failed={len(invalid_records)}")

        # Handle Invalid Data (Quarantine)
      # --- SAVE QUARANTINE (Invalid Data) ---
        if invalid_records:
            # Puranay code ki jagah naya 'save_data' function
            quarantine_path = save_data(invalid_records, "quarantine", "quarantine_errors", "json")
            logger.warning(f" {len(invalid_records)} bad records moved to: {quarantine_path}")
        # Future Step 2: Transformation
        # transform_data() <-- Kal hum ye function add karein ge
        if not valid_records:
            logger.error("No valid records to process. Stopping.")
            return
        logger.info("Step 3: Transforming Validated Data...")
        transformed_df = process_validated_data(valid_records)
        logger.info(f"  Transformed Data Shape: {transformed_df.shape}")    
        # Future Step 4: Load to Data Warehouse
        # load_data() <-- Kal hum ye function add karein ge 
        logger.info("Step 4: Saving Processed Data...")
        processed_path = save_data(transformed_df, "processed", "clean_products", "csv")
        logger.info(f"  Processed data saved at: {processed_path}")

        
        logger.info(" --- Pipeline Finished Successfully ---")
        
    except Exception as e:
        logger.critical(f" Pipeline Crashed: {e}")

if __name__ == "__main__":
    run_pipeline()