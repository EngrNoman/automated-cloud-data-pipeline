from pydantic import BaseModel, Field, EmailStr, HttpUrl, field_validator
from typing import List, Optional , Literal
from datetime import datetime


# --- SUB-SCHEMAS (Nested Objects k liye) ----
# Pehlay choti classes banayein, phir unhain main class my use karain.

class Dimensions(BaseModel):
  width: float = Field(gt=0)
  height: float = Field(gt=0)
  depth: float = Field(gt=0)

class ReviewSchema(BaseModel):
  rating: float = Field(ge=0, le=5)
  comment: str
  date: datetime
  reviewerName: str
  reviewerEmail: EmailStr # Email validation k liye

class MetaSchema(BaseModel):
  createdAt: datetime
  updatedAt: datetime
  barcode: str
  qrCode: Optional[HttpUrl] = None

#  --- MAIN PRODUCT SCHEMA ----
class ProductSchema(BaseModel):
  # 1. ID & SKU 
  id : int = Field(description="Unique identifier for the product")
  sku: str = Field(min_length=1, description="Stock Keeping Unit - Unique code for each product")
  # 2 Text Fields(Optional may be empty)
  title: Optional[str]= "Untitled Product"
  description: Optional[str]= "No description available."
  
  # 3. Category & Status (Predefined values)
  category: Literal['furniture', 'beauty', 'groceries', 'fragrances']
  brand: Optional[Literal[
  "Calvin Klein", "Gucci", "Essence", "Chanel",
  "Nail Couture", "Furniture Co.", "Bath Trends",
  "Knoll", "Glamour Beauty", "Chic Cosmetics",
  "Dolce & Gabbana", "Dior", "Velvet Touch",
  "Annibale Colombo"
  ]] = None
  availabilityStatus: Literal["In Stock",
    "Low Stock"]

  # 4. Numeric Fields
  price: float = Field(gt=0, description="Price must be a positive number")
  discountPercentage: float = Field(ge=0, le=100, description="Discount percentage must be between 0 and 100")
  rating: float = Field(ge=0, le=5, description="Rating must be between 0 and 5")
  stock: int = Field(ge=0, description="Stock must be a non-negative integer") 
  weight: float = Field(gt=0, description="Weight must be a positive number")


  # 5. list & Nested Objects
  tags: List[str] = []

  # Now use sub-schemas
  dimensions: Optional[Dimensions] = None
  reviews: List[ReviewSchema] = []
  meta: Optional[MetaSchema] = None

  # 6. Additional Fields (Optional may be empty)
  warrantyInformation: Optional[str] = None
  shippingInformation: Optional[str] = None
  returnPolicy: Optional[str] = None
  minimumOrderQuantity: int = Field(ge=0, description="Minimum order quantity must be a non-negative integer")
  images: List[HttpUrl] = []
  thumbnail: Optional[HttpUrl] = None 




# Function to validate a product record
def validate_product_dataset(raw_data_list: List[dict]):
  valid_data = []
  invalid_data = []

  seen_ids = set()
  seen_skus = set()

  for row in raw_data_list:
    try:
        # Step 1: Pydantic Validation (Format & Ranges)
        product = ProductSchema(**row)
        # Step 2: Uniqueness Check (Functional Logic)
        # Pydantic ye nahi kar sakta, is liye hum khud kar rahy hain
        if product.id in seen_ids:
            raise ValueError(f"Duplicate ID found: {product.id}")
        if product.sku in seen_skus:
            raise ValueError(f"Duplicate SKU found: {product.sku}")
        # Agar sab theek hai to save karo
        seen_ids.add(product.id)
        seen_skus.add(product.sku)
        valid_data.append(product.model_dump())
    except Exception as e:
      # Error handling
        error_report = {
            "failed_id": row.get('id', 'Unknown'),
            "error": str(e),
            "raw_data": row
         }
        invalid_data.append(error_report)
  return valid_data, invalid_data

