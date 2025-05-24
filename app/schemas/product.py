from app.models.product import AddProduct, GetProduct
from app.utils.mongo import db
from bson import ObjectId
from datetime import datetime

class ProductService:

    # Add Product 
    async def add_product(self, product: dict) -> bool:
        """
        Add Product in the database
        """
        try:
            product_data = AddProduct(**product)
            await db.product.insert_one(product_data.dict())
            return True
        
        except Exception as e:
            raise

    # Get all Products
    async def get_products(self, page, per_page) -> tuple:
        """
        Get all Products
        """
        try:
            skip_count = (page - 1) * per_page
            cursor =  db.product.find({"is_deleted":False}).skip(skip_count).limit(per_page)
            total_records = await db.product.count_documents({"is_deleted":False})
            total_pages = (total_records + per_page - 1) // per_page
            products = []
            async for product in cursor:
                product_obj = GetProduct(**product)
                products.append(product_obj.dict())
            return products, total_records, total_pages
        except Exception as e:
            raise
        

    #Get user by email for login
    async def get_product_by_id(self, product_id:str)-> dict:
        """
        Get user by email for login
        """
        try:
            product = await db.product.find_one({"_id": ObjectId(product_id), "is_deleted":False})
            if product:
                product_obj = GetProduct(**product)
                return product_obj.dict()
            return False
        except Exception as e:
            return False
        
    # Update Product
    async def update_product(self, product_id:str, product:dict) -> bool:
        """
        Update Product
        """
        try:
            filtered_product = {key: value for key, value in product.items() if value is not None}
            filtered_product["updated_at"] = datetime.utcnow()
            product = await db.product.find_one({"_id": ObjectId(product_id), "is_deleted":False})
            if product:
                await db.product.update_one({"_id": ObjectId(product_id)}, {"$set": filtered_product})
                return True
            else:
                return False
        except Exception as e:
            raise
        
    # Delete Product
    async def delete_product(self, product_id:str) -> bool:
        """
        Delete Product
        """
        try:
            await db.product.update_one(
                {"_id": ObjectId(product_id)},
                {"$set": {"is_deleted": True}}
                )
            return True
        except Exception as e:
            return False
        