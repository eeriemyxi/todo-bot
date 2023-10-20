import logging
import pprint

import tanjun

from bot.ext.tanjun.todo.scanner import TokenScanner

logger = logging.getLogger(__name__)
component = tanjun.Component()


@component.with_command
@tanjun.as_message_command("todo")
async def command_todo(ctx: tanjun.abc.MessageContext) -> None:
    logger.info("Todo command called: %s", repr(ctx.content))

    scanner = TokenScanner(ctx.content)
    tokens = scanner.scan_tokens()

    await ctx.respond(f"```py\n{pprint.pformat(tokens)}```")
