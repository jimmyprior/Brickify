import os 
import logging 

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from aiohttp import ClientSession
from motor.motor_asyncio import AsyncIOMotorClient

from .endpoints.mosaic import router as mosaic_router
from .endpoints.piecelist import router as piecelist_router
from .endpoints.piece import router as piece_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Contains logic for startup and shutdown. Adds two properties to the fastapi class:
        
        database : MongoDB agonstic database connection to brickify
        aiohttp_session : aiohttp session to be used for requests to lambda

    REF: https://fastapi.tiangolo.com/advanced/events/
    """
    #on startup
    logging.info("Starting on startup tasks")
    aiohttp_session = ClientSession(raise_for_status=True) #create the aiohttp client session
    #create the database connection
    database_client = AsyncIOMotorClient(
        os.getenv("DATABASE_URI"), 
        uuidRepresentation="standard" #uuid representation
    )
    app.database = database_client.brickify #add the database field to the FastAPI app
    app.aiohttp_session = aiohttp_session #add the aiohttp filed to the FastAPI app
    logging.info("Completed on startup tasks")
    yield
    #on shutdown
    logging.info("Starting on shutdown tasks")
    await aiohttp_session.close() #close the aiohttp client session
    logging.info("Completed on shutdown tasks")



brickify_app = FastAPI(lifespan=lifespan)

#origin_regex = "https?://([a-zA-Z0-9-]+\.)*brickify\.art"

brickify_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    #allow_origin_regex=origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

brickify_app.include_router(mosaic_router)
brickify_app.include_router(piecelist_router)
brickify_app.include_router(piece_router)

