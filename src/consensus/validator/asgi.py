from contextlib import asynccontextmanager

import fastapi

import fiber.chain.interface

from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from consensus import utils

from consensus.validator.routers.health import factory as health_factory


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
     
    app.state.substrate = fiber.chain.interface.get_substrate(
        subtensor_network=app.state.config.subtensor_network,
        subtensor_address=app.state.config.subtensor_address,
    )

    yield

    logger.info("Shutting Down...")


def factory():
    utils.setup_loguru()

    app = fastapi.FastAPI(lifespan=lifespan)
    app.state.config = utils.Config()

    app.include_router(health_factory(app))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    return app
