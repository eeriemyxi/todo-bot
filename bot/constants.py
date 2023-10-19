from pathlib import Path

import yaml
from hikari import Intents

with open("configuration.yml") as config:
    CONFIG = yaml.safe_load(config)

BOT_TOKEN = CONFIG["bot"]["token"]
BOT_INTENTS = (
    Intents.MESSAGE_CONTENT
    | Intents.GUILDS
    | Intents.GUILD_EMOJIS
    | Intents.GUILD_INTEGRATIONS
    | Intents.GUILD_MESSAGES
    | Intents.GUILD_MODERATION
)
BOT_DEFAULT_COMMAND_PREFIX = ""

REGISTERED_TANJUN_EXTENSIONS: tuple[str, ...] = ("todo",)
TANJUN_EXTENSIONS_DIRECTORY: Path = Path("bot/ext/tanjun")
