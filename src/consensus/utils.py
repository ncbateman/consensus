import datetime
import hmac
import logging
import sys

import fastapi
import fastapi.openapi.utils
import pydantic
import pydantic_settings

from loguru import logger


AUTHORIZATION = fastapi.security.APIKeyHeader(name="Authorization", auto_error=False)

class Config(pydantic_settings.BaseSettings):
    model_config = {"env_file": ".env"}

    redis_url: pydantic.RedisDsn

    debug: bool = pydantic.Field(default=False)

    # bittensor stuff
    subtensor_network: str = pydantic.Field(default="finney")
    subtensor_address: str = pydantic.Field(default="wss://entrypoint-finney.opentensor.ai:443")



async def get_substrate(request: fastapi.Request):
    """
    Extract a reference to the substrate interface.
    """
    yield request.app.state.substrate


async def get_config(request: fastapi.Request):
    """
    Extract a reference to the application Config.
    """
    yield request.app.state.config

def hmac_generate(secret_key: str, payload: str) -> str:
    """
    Generate an hmac of the provided payload.
    """
    return hmac.HMAC(bytes.fromhex(secret_key), payload.encode(), "sha256").hexdigest()


def hmac_verify(secret_key: str, payload: str, signature: str) -> bool:
    """
    Generate an hmac of the provided payload and verify it against the signature.
    """
    return hmac_generate(secret_key, payload) == signature


def now(*, precise: bool = False):
    """
    Get an ISO8601 UTC timestamp. Unless precise == True, it will truncate to
    the second.
    """
    ts = datetime.datetime.now(tz=datetime.UTC)
    if not precise:
        ts = ts.replace(microsecond=0)
    return ts

def setup_loguru(level="INFO"):
    class PropagateHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            record.extra = []  # it's normally a dict, OTEL prefers a list
            logging.getLogger(record.name).handle(record)

    logger.remove()
    logger.add(sink=sys.stdout, level=level)
    logger.add(PropagateHandler(), level=level, format="{message}")

