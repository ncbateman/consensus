import asyncio
import functools
import typer
import uvicorn

from consensus.metagraph.refresh import metagraph_refresh
from consensus.miner import asgi as miner_asgi
from consensus.validator import asgi as validator_asgi


cli = typer.Typer(
    name="consensus",
    pretty_exceptions_enable=False,
)


def run_async(fn):
    @functools.wraps(fn)
    def inner(*args, **kwargs):
        return asyncio.run(fn(*args, **kwargs))

    return inner

@cli.command("metagraph")
def cli_metagraph():
    metagraph_refresh()

@cli.command("validator")
def cli_miner(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(
        app=validator_asgi.factory(),
        host=host,
        port=port,
    )

@cli.command("miner")
def cli_miner(host: str = "0.0.0.0", port: int = 8001):
    uvicorn.run(
        app=miner_asgi.factory(),
        host=host,
        port=port,
    )


def main():
    cli()


if __name__ == "__main__":
    main()
