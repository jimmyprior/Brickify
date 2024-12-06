from typing import Annotated

from fastapi import Request
from aiohttp import ClientSession
from motor.core import AgnosticDatabase

def get_database(request : Request) -> AgnosticDatabase:
    """
    request the database connection stored in the fastapi app
    """
    app = request.app #fastapi app 
    #on startup will set the database 
    return app.database # should have been set by the startup


def get_aiohttp_session(request : Request) -> ClientSession:
    """
    gets global aiohttp client session
    """
    app = request.app #fastapi app 
    #on startup will create the client session 
    return app.aiohttp_session # should have been set by the startup

