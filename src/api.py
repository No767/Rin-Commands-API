#!/usr/bin/env python3
import sys
from pathlib import Path

from fastapi import FastAPI, Response, status

from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi.openapi.utils import get_openapi

mainPath = Path(__file__).parents[1]
sys.path.append(str(mainPath))

from api_utils import CrudMethods
from api_utils.db import SessionLocal

tagsMetadata = [{"name": "Obtain Commands", "description": "Gets the list of commands that Rin has"}]
app = FastAPI(openapi_tags=tagsMetadata, redoc_url=None)
utils = CrudMethods()

description = """
# Overview
An API to fetch the commands that Rin actively has since v2.2. This is meant to be a private API.

# GitHub
For Rin, refer to the GitHub Repo [here](https://github.com/No767/Rin)
"""
def rin_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Rin Commands",
        version="0.1.0",
        description=description,
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://raw.githubusercontent.com/No767/Rin/dev/assets/rin-logo.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = rin_openapi

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
        
@app.get("/", include_in_schema=False)
async def docs_redirect():
    return RedirectResponse(url='/docs')

@app.get("/commands/all", response_class=ORJSONResponse, tags=["Obtain Commands"], description="Literally get all of the commands Rin has")
async def get_all_commands(response: Response):
    result = await utils.get_all_commands()
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": response.status_code, "message": "No commands found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"status": response.status_code, "count": len(result), "data": result}

@app.get("/commands/{module}", response_class=ORJSONResponse, tags=["Obtain Commands"], description="Gets the commands for a specific module or cog from Rin")
async def get_module_commands(response: Response, module: str):
    res = await utils.get_all_commands_from_module(module=module)
    if len(res) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": response.status_code, "message": "No commands found within that module"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"status": response.status_code, "count": len(res), "data": res}