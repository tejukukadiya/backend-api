from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import List, Union
from pydantic import validator
import os

load_dotenv()

class Settings(BaseSettings):
   
    MONGO_URI: str = os.environ.get("MONGO_URL")
    MONGO_DB_NAME : str = os.environ.get("MONGO_DB_NAME")
    AES_KEY:str =os.environ.get("AES_KEY")
    IV_KEY:str =os.environ.get("IV_KEY")
    SECRET_KEY: str =os.environ.get("SECRET_KEY")
    ALGORITHM :str =os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_TIME: str = os.environ.get("ACCESS_TOKEN_EXPIRE_TIME")

    BACKEND_CORS_ORIGINS: List = []

    @validator("BACKEND_CORS_ORIGINS", pre=True, allow_reuse=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    STATIC_FILE :str= "static"

settings = Settings()
