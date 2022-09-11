#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import redis.asyncio as redis
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import ORJSONResponse, RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from prometheus_fastapi_instrumentator import Instrumentator
from redis.asyncio.connection import ConnectionPool
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

mainPath = Path(__file__).parents[1]
sys.path.append(str(mainPath))

from api_utils import CrudMethods
from api_utils.db import SessionLocal

load_dotenv()

REDIS_SERVER_IP = os.getenv("Redis_Server_IP")
REDIS_SERVER_PORT = os.getenv("Redis_Port")

tagsMetadata = [
    {
        "name": "Obtain Commands",
        "description": "Gets the list of commands that Rin has",
    },
    {"name": "Metrics", "description": "Exporter for Prometheus metrics"},
    {"name": "Modules", "description": "Gets the list of modules that Rin has"},
]

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["75/hour"],
    storage_uri=f"redis://{REDIS_SERVER_IP}:{REDIS_SERVER_PORT}/1",
)
app = FastAPI(openapi_tags=tagsMetadata, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
utils = CrudMethods()

description = """
# Overview
An API to fetch the commands that Rin actively has since v2.2. This is meant to be a private API.

# Rate Limiting

The default rate limiting for all endpoints is **75** requests per hour.
# GitHub
[Rin](https://github.com/No767/Rin)
[Rin-Commands-API](https://github.com/No767/Rin-Commands-API)
"""


def rin_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Rin Commands",
        version="0.2.1",
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
    return RedirectResponse(url="/docs")


@app.get(
    "/commands/all",
    response_class=ORJSONResponse,
    tags=["Obtain Commands"],
    description="Literally get all of the commands Rin has",
)
@cache(namespace="get_all_commands", expire=3600)
async def get_all_commands(request: Request, response: Response):
    result = await utils.get_all_commands()
    if len(result) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": response.status_code, "message": "No commands found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"status": response.status_code, "count": len(result), "data": result}


@app.get(
    "/commands/{module}",
    response_class=ORJSONResponse,
    tags=["Obtain Commands"],
    description="Gets the commands for a specific module or cog from Rin",
)
@cache(namespace="get_module_commands", expire=3600)
async def get_module_commands(request: Request, response: Response, module: str):
    res = await utils.get_all_commands_from_module(module=module)
    if len(res) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            "status": response.status_code,
            "message": "No commands found within that module",
        }
    else:
        response.status_code = status.HTTP_200_OK
        return {"status": response.status_code, "count": len(res), "data": res}


@app.get(
    "/modules/all",
    response_class=ORJSONResponse,
    tags=["Modules"],
    description="Gets all of the modules that Rin has",
)
@cache(namespace="get_available_modules", expire=3600)
async def get_all_modules(request: Request, response: Response):
    mainRes = await utils.get_modules()
    if len(mainRes) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": response.status_code, "message": "No modules found"}
    else:
        response.status_code = status.HTTP_200_OK
        return {"status": response.status_code, "count": len(mainRes), "data": mainRes}


@app.on_event("startup")
async def startup():
    pool = ConnectionPool.from_url(
        url=f"redis://{REDIS_SERVER_IP}", encoding="utf-8", decode_responses=True
    )
    r = redis.Redis(connection_pool=pool)
    FastAPICache.init(RedisBackend(r), prefix="rin-cache")
    Instrumentator().instrument(app).expose(app, endpoint="/metrics", tags=["Metrics"])
