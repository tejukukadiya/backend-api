from app.models.category import AddCategory,GetCategory
from app.utils.mongo import db
from bson import ObjectId
from datetime import datetime

class Category:

  async def add_category(self,category:dict)->bool:
    try:
      category_data=AddCategory(**category)
      await db.category.insert_one(category_data.dict())
      return True
    
    except Exception as e:
      raise

  async def get_category(self,page,per_page) -> tuple:
    try:
      skip_count = (page - 1) * per_page
      cursor=db.category.find({"is_deleted":False}).skip(skip_count).limit(per_page)
      total_records=await db.category.count_documents({"is_deleted":False})
      total_pages = (total_records + per_page - 1) // per_page
      categories=[]
      async for category in cursor:
        category_obj=GetCategory(**category)
        categories.append(category_obj.dict())
      return categories,total_pages,total_records
    except Exception as e:
      raise

  async def get_category_by_id(self,category_id:str)->dict:
    try:
      category = await db.category.find_one({"_id": ObjectId(category_id), "is_deleted":False})
      if category:
        category_obj = GetCategory(**category)
        return category_obj.dict()
      return False
    except Exception as e:
            return False
    
  async def update_category(self, category_id:str, category:dict) -> bool:
    try:
      filtered_category = {key: value for key, value in category.items() if value is not None}
      filtered_category["updated_at"] = datetime.utcnow()
      category = await db.category.find_one({"_id": ObjectId(category_id), "is_deleted":False})
      if category:
        await db.category.update_one({"_id": ObjectId(category_id)}, {"$set": filtered_category})
        return True
      else:
        return False
    except Exception as e:
        raise
  
  async def delete_category(self, category_id:str) -> bool:
    try:
      await db.category.update_one(
          {"_id": ObjectId(category_id)},
          {"$set": {"is_deleted": True}}
                )
      return True
    except Exception as e:
            return False

  






  

