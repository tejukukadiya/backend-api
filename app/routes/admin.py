from fastapi import APIRouter,Depends,HTTPException
from datetime import timedelta
from app.models.admin import AdminCreate,Token,LoginRequest
from app.utils.mongo import db
from app.schemas.admin import authenticate_admin,hash_password,create_token
from bson import ObjectId

ACCESS_TOKEN_EXPIRE_MINUTES = 60

admin_router = APIRouter()

@admin_router.post("/register")
async def register(admin: AdminCreate):
    if await db["admin"].find_one({"username":admin.username}):
        raise HTTPException(status_code=400, detail="Admin already exists")
    hashed = hash_password(admin.password)
    await db["admin"].insert_one({
        "username": admin.username,
        "email": admin.email,
        "hashed_password": hashed
    })
    return {"msg": "Admin registered succesfully"}

@admin_router.post("/login", response_model=Token)
async def login(data: LoginRequest):
    admin = await authenticate_admin(data.username, data.password)
    if not admin:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token_expires = timedelta(minutes=60)
    token = create_token({"sub": admin.username}, expires_delta=token_expires)
    return {"access_token": token, "token_type": "bearer"}

@admin_router.get("/")
async def get_all_admins():
    admins_cursor = db["admin"].find({}, {"_id": 0, "hashed_password": 0})  
    admins = await admins_cursor.to_list(length=None)
    return admins

from bson import ObjectId

@admin_router.get("/{admin_id}")
async def get_admin_by_id(admin_id: str):
    try:
        admin = await db["admin"].find_one(
            {"_id": ObjectId(admin_id)},
            {"_id": 1, "username": 1, "email": 1}
        )
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        admin["id"] = str(admin["_id"])
        del admin["_id"]
        return admin
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID format")



@admin_router.put("/{admin_id}")
async def update_admin(admin_id: str, updated_admin: AdminCreate):
    existing = await db["admin"].find_one({"_id":ObjectId(admin_id) })
    if not existing:
        raise HTTPException(status_code=404, detail="Admin not found")

    hashed_pw = hash_password(updated_admin.password)
    updated_data = {
        "username": updated_admin.username,
        "email": updated_admin.email,
        "hashed_password": hashed_pw,
    }

    await db["admin"].update_one({"_id":ObjectId(admin_id)}, {"$set": updated_data})
    return {"msg": "Admin updated successfully"}

@admin_router.delete("/{admin_id}")
async def delete_admin(admin_id: str):
    result = await db["admin"].delete_one({"_id":ObjectId(admin_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Admin not found")
    return {"msg": "Admin deleted successfully"}
