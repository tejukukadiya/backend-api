from pydantic import BaseModel,Field,validator,root_validator
from typing import Optional
from datetime import datetime
from bson import ObjectId
import json

class CreateCategory(BaseModel):
  category_name:Optional[str] = Field(None)

class AddCategory(CreateCategory):
  created_at:datetime=Field(default_factory=datetime.utcnow)
  updated_at:datetime=Field(default_factory=datetime.utcnow)
  is_deleted:bool=Field(default=False)

class GetCategory(BaseModel):
  id:str=Field(alias="_id")
  category_name:Optional[str] = Field(default=None)
  created_at:Optional[datetime]=None
  updated_at:Optional[datetime]=None

  @root_validator(pre=True)
  def parse_id_to_str(cls, values):
    if "_id" in values and isinstance(values["_id"], ObjectId):
      values["_id"] = str(values["_id"])
    return values

  @validator("created_at")
  def convert_created_at_to_str(cls,value):
    if isinstance(value,datetime):
      return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)

  @validator("updated_at")
  def convert_updated_at_to_str(cls,value):
    if isinstance(value,datetime):
      return value.strftime("%Y-%m-%d %H:%M:%S")
    return str(value)

