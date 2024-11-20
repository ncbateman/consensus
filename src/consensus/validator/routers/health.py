from typing import Literal

import fastapi
from loguru import logger

from consensus import utils

def health_endpoint ():
    return {"status": "ok"}

def factory(app: fastapi.FastAPI) -> fastapi.APIRouter:

    methods = ["POST", "GET"]

    router = fastapi.APIRouter()

    router.add_api_route(
        "/health",
        health_endpoint,
        tags=["health"],
        methods=methods
    )

    return router
