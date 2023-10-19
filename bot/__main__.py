import logging
from pathlib import Path

import hikari
import tanjun
from rich.logging import RichHandler

from bot import constants
from bot.ext.db.core import BaseDatabase

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)


def load_tanjun_extensions(
    logger: logging.Logger,
    client: tanjun.abc.Client,
    mods: tuple[str, ...],
    mod_dir: Path,
) -> None:
    for mod in mod_dir.glob("*.py"):
        if mod.with_suffix("").name in mods:
            client.load_modules(mod)
        else:
            logger.info(
                "Found `%s` in `%s`, but it is unregistered as a module. "
                "Loading cancelled.",
                mod.name,
                mod_dir,
            )


def main() -> None:
    bot = hikari.GatewayBot(intents=constants.BOT_INTENTS, token=constants.BOT_TOKEN)
    database = BaseDatabase()

    tanjun_client = (
        tanjun.Client.from_gateway_bot(bot)
        .add_prefix(constants.BOT_DEFAULT_COMMAND_PREFIX)
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, database.connect)
    )

    load_tanjun_extensions(
        logger,
        tanjun_client,
        constants.REGISTERED_TANJUN_EXTENSIONS,
        constants.TANJUN_EXTENSIONS_DIRECTORY,
    )

    bot.run()


if __name__ == "__main__":
    main()
