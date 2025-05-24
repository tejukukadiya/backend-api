from fastapi import APIRouter, status, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from app.utils.auth import encrypt, decrypt, create_access_token
from app.core.config import settings
from app.models.product import CreateProduct
from app.schemas.product import ProductService
from app.utils.auth import get_current_user
import logging

logger = logging.getLogger('fastapi')

product_router = APIRouter()
# Product APIS

# Create Product
@product_router.post("/")
async def create_product(request:Request, product: CreateProduct, current_user = Depends(get_current_user)):
    try:
        user_id = current_user["_id"]
        logger.info(f"{user_id} added product: {product.product_name} - {request.method} - {request.url}")
        product_service = ProductService()
        await product_service.add_product(product.dict())
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "status" : True,
                "data" : "Product added successfully",
            }
        )
    except Exception as e:
        logger.error(f"Error in create_product: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )
        
# Get all products
@product_router.get("/")
async def get_products(request:Request, page:int= 1, per_page:int= 10,current_user = Depends(get_current_user)):
    try:
        user_id = current_user["_id"]
        logger.info(f"{user_id} fetched all products - {request.method} - {request.url}")
        product_service = ProductService()
        products, total_records, total_pages = await product_service.get_products(page, per_page)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status" : True,
                "data" : products,
                "total_records" : total_records,
                "total_pages" : total_pages,
                "current_page" : page,
                "message" : "Products fetched successfully"
            }
        )
    except Exception as e:
        logger.error(f"Error in get_products: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )
        
# Get product by id
@product_router.get("/{product_id}")
async def get_product_by_id(request:Request, product_id:str, current_user = Depends(get_current_user)):
    try:
        user_id = current_user["_id"]
        logger.info(f"{user_id} fetched product with id: {product_id} - {request.method} - {request.url}")
        product_service = ProductService()
        product = await product_service.get_product_by_id(product_id)
        if product:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status" : True,
                    "data" : product,
                    "message" : "Product fetched successfully"
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status" : False,
                    "data" : "Product does not exist with this id"
                }
            )
    except Exception as e:
        logger.error(f"Error in get_product_by_id: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )
        
# Update product by id
@product_router.put("/{product_id}")
async def update_product_by_id(request:Request, product_id:str, product: CreateProduct, current_user = Depends(get_current_user)):
    try:
        user_id = current_user["_id"]
        logger.info(f"{user_id} updated product with id: {product_id} - {request.method} - {request.url}")
        product_service = ProductService()
        product = await product_service.update_product(product_id, product.dict())
        if product:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status" : True,
                    "message" : "Product updated successfully"
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status" : False,
                    "data" : "Product does not exist with this id"
                }
            )
    except Exception as e:
        logger.error(f"Error in update_product_by_id: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )
        
# Delete product by id
@product_router.delete("/{product_id}")
async def delete_product_by_id(request:Request, product_id:str, current_user = Depends(get_current_user)):
    try:
        user_id = current_user["_id"]
        logger.info(f"{user_id} deleted product with id: {product_id} - {request.method} - {request.url}")
        product_service = ProductService()
        product = await product_service.delete_product(product_id)
        if product:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "status" : True,
                    "data" : product,
                    "message" : "Product deleted successfully"
                }
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "status" : False,
                    "data" : "Product does not exist with this id"
                }
            )
    except Exception as e:
        logger.error(f"Error in delete_product_by_id: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "status" : False,
                "data" : "Internal Server Error"
            }
        )