import os
import uvicorn
import logging

from backend.v1.api import brickify_app

logging.basicConfig(
    filename="brickifyapp.log",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

if __name__ == "__main__":
    uvicorn.run(
        "main:brickify_app", 
        port=5000, 
        log_level="info", 
        host="127.0.0.1",
        reload=bool(os.getenv("DEVELOPMENT", True))
    )