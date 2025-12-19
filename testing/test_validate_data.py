import sys
import os
import json

# Path Setup: Taake hum andar waly folders se import kar sakein
import sys
import os

# --- PATH SETUP (Import se pehlay zaroori hai) ---

# 1. Is file (test.py) ka folder pata karo (yani 'testing' folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Ek step peeche jao (yani 'Root' folder)
root_dir = os.path.dirname(current_dir)

# 3. Root folder ko Python k rasto (sys.path) mein shamil karo
sys.path.append(root_dir)

# ... Baki code wesa hi rahay ga ...

# Humara Validator Import karein
from src.transformation.validator import validate_product_dataset as validate_dataset

# ==========================================
# MOCK DATA (Testing Scenarios)
# ==========================================
# Hum 4 records banayen ge: 1 Sahi, 3 Ghalat

raw_test_data = [
    # CASE 1: ✅ Perfect Record (Happy Path)
    {
            "id": 1,
            "title": "Essence Mascara Lash Princess",
            "description": "The Essence Mascara Lash Princess is a popular mascara known for its volumizing and lengthening effects. Achieve dramatic lashes with this long-lasting and cruelty-free formula.",
            "category": "beauty",
            "price": 9.99,
            "discountPercentage": 10.48,
            "rating": 2.56,
            "stock": 99,
            "tags": [
                "beauty",
                "mascara"
            ],
            "brand": "Essence",
            "sku": "BEA-ESS-ESS-001",
            "weight": 4,
            "dimensions": {
                "width": 15.14,
                "height": 13.08,
                "depth": 22.99
            },
            "warrantyInformation": "1 week warranty",
            "shippingInformation": "Ships in 3-5 business days",
            "availabilityStatus": "In Stock",
            "reviews": [
                {
                    "rating": 3,
                    "comment": "Would not recommend!",
                    "date": "2025-04-30T09:41:02.053Z",
                    "reviewerName": "Eleanor Collins",
                    "reviewerEmail": "eleanor.collins@x.dummyjson.com"
                },
                {
                    "rating": 4,
                    "comment": "Very satisfied!",
                    "date": "2025-04-30T09:41:02.053Z",
                    "reviewerName": "Lucas Gordon",
                    "reviewerEmail": "lucas.gordon@x.dummyjson.com"
                },
                {
                    "rating": 5,
                    "comment": "Highly impressed!",
                    "date": "2025-04-30T09:41:02.053Z",
                    "reviewerName": "Eleanor Collins",
                    "reviewerEmail": "eleanor.collins@x.dummyjson.com"
                }
            ],
            "returnPolicy": "No return policy",
            "minimumOrderQuantity": 48,
            "meta": {
                "createdAt": "2025-04-30T09:41:02.053Z",
                "updatedAt": "2025-04-30T09:41:02.053Z",
                "barcode": "5784719087687",
                "qrCode": "https://cdn.dummyjson.com/public/qr-code.png"
            },
            "images": [
                "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/1.webp"
            ],
            "thumbnail": "https://cdn.dummyjson.com/product-images/beauty/essence-mascara-lash-princess/thumbnail.webp"
        }
    ]

# ==========================================
# EXECUTION
# ==========================================

print("🚀 Running Validation Tests...\n")

valid_records, invalid_records = validate_dataset(raw_test_data)

# --- REPORTING ---

print(f"✅ PASSED: {len(valid_records)}")
print(f"❌ FAILED: {len(invalid_records)}")

print("\n--- 🔍 Failure Analysis (Why did they fail?) ---")
for i, record in enumerate(invalid_records, 1):
    print(f"\n[Case {i}] ID: {record['failed_id']}")
    print(f"Reason: {record['error']}")

# Optional: Invalid records ko JSON my save kar k dekhein
if invalid_records:
    with open("validation_errors.json", "w") as f:
        json.dump(invalid_records, f, indent=4)
    print("\n📁 Errors saved to 'validation_errors.json'")