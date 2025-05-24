from pydantic import BaseModel,Field, validator, root_validator
from datetime import datetime
from typing import Optional
import json
from bson import ObjectId

class CreateProduct(BaseModel):
    product_name: Optional[str] = Field(None)
    company_name: Optional[str] = Field(None)
    
class AddProduct(CreateProduct):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)  
    is_deleted: bool = Field(default=False)
    
class GetProduct(BaseModel):
    id: str = Field(alias="_id")
    product_name: Optional[str] = Field(...)
    company_name: Optional[str] = Field(default=None)
    created_at: datetime
    updated_at: datetime
    
    @root_validator(pre=True)
    def parse_id_to_str(cls, values):
        if "_id" in values and isinstance(values["_id"], ObjectId):
            values["_id"] = str(values["_id"])
        return values
    
    @validator("created_at")
    def convert_created_at_to_string(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)
    
    @validator("updated_at")
    def convert_updated_at_to_string(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return str(value)