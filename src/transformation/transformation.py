import pandas as pd
import json

def process_validated_data(valid_data_list):
    """
    Input: valid_data_list (List of Dicts from Pydantic .model_dump(mode='json'))
    Output: Clean Pandas DataFrame ready for CSV/Redshift/SQL.
    """
    
    if not valid_data_list:
        print("⚠️ No valid data to process.")
        return pd.DataFrame()

    # 1. Load Data
    df = pd.DataFrame(valid_data_list)
    print(f"--- Processing {len(df)} Valid Records ---")

    # ---------------------------------------------------------
    # STEP 1: FLATTEN NESTED OBJECTS (Backend Logic)
    # ---------------------------------------------------------
    
    # A. Handle 'dimensions' (width, height, depth alag columns banayenge)
    if 'dimensions' in df.columns:
        # Check if data exists, then extract keys to new columns
        # Note: 'apply(pd.Series)' dictionary ko columns mein tor deta hai
        dims_df = df['dimensions'].apply(pd.Series).add_prefix('dimensions_')
        df = pd.concat([df, dims_df], axis=1)
        df.drop(columns=['dimensions'], inplace=True) # Original nested column remove

    # B. Handle 'meta' (createdAt, barcode waghaira nikalna)
    if 'meta' in df.columns:
        meta_df = df['meta'].apply(pd.Series)
        # Rename specific meta columns if needed (e.g. barcode -> meta_barcode)
        meta_df.columns = [f"meta_{col}" for col in meta_df.columns]
        df = pd.concat([df, meta_df], axis=1)
        df.drop(columns=['meta'], inplace=True)

    # ---------------------------------------------------------
    # STEP 2: SERIALIZE COMPLEX LISTS (JSON Strings for CSV/SQL)
    # ---------------------------------------------------------
    # Lists (Arrays) CSV mein save nahi ho sakti, unhe string banana parta hai.
    
    complex_cols = ['tags', 'reviews', 'images']
    
    for col in complex_cols:
        if col in df.columns:
            # Har list ko JSON string mein convert karo
            # default=str rakhna zaroori hai taake agar koi Date/Url object ho to error na aye
            df[col] = df[col].apply(lambda x: json.dumps(x, default=str))

    # ---------------------------------------------------------
    # STEP 3: TEXT FORMATTING (Cosmetic)
    # ---------------------------------------------------------
    
    # A. Titles & Brands (Title Case: "Iphone 13 Pro")
    title_cols = ['title', 'brand', 'warrantyInformation', 'returnPolicy', 'availabilityStatus']
    for col in title_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()
            
    # B. Description (Sentence Case: "This is a product...")
    # Title case description par acha nahi lagta, isliye sirf pehla lafz bara karein.
    if 'description' in df.columns:
        df['description'] = df['description'].astype(str).str.strip().apply(
            lambda x: x.capitalize() if x else "No description available"
        )

    # C. URL Cleaning (Ensure Thumbnail is string)
    if 'thumbnail' in df.columns:
        df['thumbnail'] = df['thumbnail'].astype(str)

    # ---------------------------------------------------------
    # STEP 4: FINAL CLEANUP
    # ---------------------------------------------------------
    if 'meta_barcode' in df.columns:
        # Isay Zabardasti String banao taake 'E+12' na aye
        df['meta_barcode'] = df['meta_barcode'].astype(str).replace(r'\.0$', '', regex=True)
    
    # Optional: Reorder columns (ID pehle aye)
    cols = list(df.columns)
    if 'id' in cols:
        cols.insert(0, cols.pop(cols.index('id')))
        df = df[cols]

    print("--- Data Transformation Completed: Ready for Storage ---")
    return df

# --- Kaisy Use Karna Hai ---
# final_df = finalize_data_for_storage(valid_data) # 'valid_data' pydantic wala list hai
# final_df.to_csv("clean_products_final.csv", index=False)