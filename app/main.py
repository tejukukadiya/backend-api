import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import api_router

# Create a FastAPI instance
app = FastAPI(
    title= "Fast API" ,
    description= "Fast API" ,
    version= "0.1.0" ,
)

class RequestLogHandler(logging.Handler):
    def emit(self, record):
        request_info = f"{record.method} {record.url}"
        record.msg = f"{request_info} - {record.getMessage()}"
        super(RequestLogHandler, self).emit(record)

logging.basicConfig(level=logging.INFO, 
                    filename='fastapi.log', 
                    filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("fastapi")

console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"] ,
    allow_credentials= True ,
    allow_methods= ["*"] ,
    allow_headers= ["*"] ,
)

app.include_router(api_router, prefix= "/api" )


@app.on_event( "startup" )
async def startup_event():
    try:
        print( "Starting up..." )
    except Exception as e:
        print( "Error: " , e)
    
@app.get( "/" )
async def root():
    return { "status": 200, "message":"Server running" }
