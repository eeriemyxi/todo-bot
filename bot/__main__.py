import logging

import hikari
import tanjun
from rich.logging import RichHandler

from bot import constants
from bot.ext.db.core import BaseDatabase

logging.basicConfig(
    level=logging.INFO, format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
)


def main() -> None:
    bot = hikari.GatewayBot(intents=constants.BOT_INTENTS, token=constants.BOT_TOKEN)
    database = BaseDatabase()

    (
        tanjun.Client.from_gateway_bot(bot)
        .add_prefix("")
        .load_modules("bot.modules.todo")
        .add_client_callback(tanjun.ClientCallbackNames.STARTING, database.connect)
    )

    bot.run()


if __name__ == "__main__":
    main()
