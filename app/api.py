from fastapi import APIRouter

from app.routes.user import user_router
from app.routes.product import product_router
from app.routes.category import category_router


api_router = APIRouter()

api_router.include_router(user_router, prefix= "/user", tags=['user'] )
api_router.include_router(product_router, prefix= "/product", tags=['product'] )
api_router.include_router(category_router, prefix= "/category", tags=['category'] )