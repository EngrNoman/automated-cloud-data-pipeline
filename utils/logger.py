import logging
import os
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass #

# Environment Check
ENV = os.getenv("ENV_TYPE", "local")
LOG_DIR = "logs"

def get_logger(module_name, logger_name=None):
    
    # Logger name set karna (Best practice)
    if logger_name is None:
        logger_name = module_name

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Agar handlers pehly se hain to dubara add mat karo (Duplicate logs fix)
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] [%(name)s] - %(message)s')

        # --- HANDLER 1: StreamHandler (Ye Local aur Cloud dono k liye zaroori hai) ---
        # Ye screen par print karega, jisy CloudWatch capture kar lega
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # --- HANDLER 2: FileHandler (SIRF LOCAL K LIYE) ---
        if ENV == "local":
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)
            
            today_date = datetime.now().strftime("%Y-%m-%d")
            log_file_name = f"pipeline_{today_date}.log"
            log_file_path = os.path.join(LOG_DIR, log_file_name)

            file_handler = logging.FileHandler(log_file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger