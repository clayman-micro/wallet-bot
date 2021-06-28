import asyncio
import socket

import click
import orjson
import pkg_resources
import structlog
import uvloop

from bot.app import BotConfig


structlog.configure(
    cache_logger_on_first_use=True,
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(serializer=orjson.dumps),
    ],
    logger_factory=structlog.BytesLoggerFactory(),
)


@click.group()
@click.pass_context
def server(ctx):
    pass


@server.command()
@click.option("--host", default=None, help="Specify application host")
@click.option("--port", default=5000, help="Specify application port")
@click.pass_context
def run(ctx, host, port):
    logger = ctx.obj["logger"]

    logger.info(f"Bot serving on http://127.0.0.1:{port}")


@click.group()
@click.option("--debug", is_flag=True, default=False)
@click.pass_context
def cli(ctx, debug: bool = False) -> None:
    uvloop.install()
    loop = asyncio.get_event_loop()

    config = BotConfig(defaults={"debug": debug})

    distrubution = pkg_resources.get_distribution("wallet-bot")

    logger = structlog.get_logger(app_name="wallet-bot", hostname=socket.gethostname(), version=distrubution.version,)

    ctx.obj["config"] = config
    ctx.obj["logger"] = logger
    ctx.obj["loop"] = loop


cli.add_command(server, name="server")


if __name__ == "__main__":
    cli(obj={})
