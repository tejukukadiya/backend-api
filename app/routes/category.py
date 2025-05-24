from fastapi import APIRouter,Request,Depends,status,HTTPException
from app.models.category import CreateCategory
from app.utils.auth import encrypt, decrypt, create_access_token
from app.core.config import settings
from app.schemas.category import Category
from fastapi.responses import JSONResponse
from app.utils.auth import get_current_user

import logging

logger = logging.getLogger('fastapi')

category_router=APIRouter()

@category_router.post("/")
async def create_category(request:Request,categories:CreateCategory,current_user=Depends(get_current_user)):
  try:
      user_id = current_user["_id"]
      logger.info(f"{user_id} added category: {categories.category_name} - {request.method} - {request.url}")
      category= Category()
      await category.add_category(categories.dict())
      return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
              "status" : True,
              "data" : "category added successfully",
        }
      )
  except Exception as e:
      logger.error(f"Error in create_category: {e}")
      return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status" : False,
            "data" : "Internal Server Error"
            }
        )

@category_router.get("/")
async def get_category(request:Request, page:int= 1, per_page:int= 10,current_user = Depends(get_current_user)):
  try:
      user_id = current_user["_id"]
      logger.info(f"{user_id} fetched all category- {request.method} - {request.url}")
      category = Category()
      categories, total_pages, total_records = await category.get_category(page, per_page)
      return JSONResponse(
          status_code=status.HTTP_200_OK,
          content={
              "status" : True,
              "data" : categories,
              "total_records" : total_records,
              "total_pages" : total_pages,
              "current_page" : page,
              "message" : "categories fetched successfully"
          }
      )
  except Exception as e:
      logger.error(f"Error in get_category: {e}")
      return JSONResponse(
          status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
          content={
              "status" : False,
              "data" : "Internal Server Error"
          }
      )
    
@category_router.get("/{category_id}")
async def get_category_by_id(request:Request, category_id:str, current_user = Depends(get_current_user)):
    try:
      user_id = current_user["_id"]
      logger.info(f"{user_id} fetched category with id: {category_id} - {request.method} - {request.url}")
      category = Category()
      categories= await category.get_category_by_id(category_id)
      if categories:
        return JSONResponse(
          status_code=status.HTTP_200_OK,
          content={
                "status" : True,
                "data" : categories,
                "message" : "Categories fetched successfully"
                }
            )
      else:
        return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
            "status" : False,
            "data" : "Category does not exist with this id"
                }
            )
    except Exception as e:
        logger.error(f"Error in get_category_by_id: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )
    
@category_router.put("/{category_id}")
async def update_category_by_id(request:Request, category_id:str, update: CreateCategory, current_user = Depends(get_current_user)):
    try:
      user_id = current_user["_id"]
      logger.info(f"{user_id} updated category with id: {category_id} - {request.method} - {request.url}")
      category = Category()
      update= await category.update_category(category_id, update.dict())
      if update:
        return JSONResponse(
          status_code=status.HTTP_200_OK,
          content={
            "status" : True,
            "message" : "category updated successfully"
                }
            )
      else:
        return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
                "status" : False,
                "data" : "Category does not exist with this id"
                }
            )
    except Exception as e:
      logger.error(f"Error in update_category_by_id: {e}")
      return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status" : False,
            "data" : "Internal Server Error"
            }
        )

@category_router.delete("/{category_id}")
async def delete_category_by_id(request:Request, category_id:str, current_user = Depends(get_current_user)):
    try:
      user_id = current_user["_id"]
      logger.info(f"{user_id} deleted category with id: {category_id} - {request.method} - {request.url}")
      category = Category()
      delete= await category.delete_category(category_id)
      if delete:
        return JSONResponse(
          status_code=status.HTTP_200_OK,
          content={
              "status" : True,
              "data" : delete,
              "message" : "category deleted successfully"
                }
            )
      else:
        return JSONResponse(
          status_code=status.HTTP_400_BAD_REQUEST,
          content={
                "status" : False,
                "data" : "category does not exist with this id"
                }
            )
    except Exception as e:
      logger.error(f"Error in delete_category_by_id: {e}")
      return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
              "status" : False,
              "data" : "Internal Server Error"
            }
        )
    
