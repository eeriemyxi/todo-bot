import pprint

import tanjun

from bot.ext.struct import (
    AtKeyword,
    Day,
    DoKeyword,
    Time,
    Token,
    TokenType,
    WhenKeyword,
)

component = tanjun.Component()


@component.with_command
@tanjun.with_greedy_argument("content")
@tanjun.as_message_command("todo")
async def command_todo(ctx: tanjun.abc.Context, content: str) -> None:
    raw_tokens = content.casefold().split()
    tokens = []

    for index, token in enumerate(raw_tokens):
        if token == "when":
            day = Day.TODAY if raw_tokens[index + 1] == "today" else Day.TOMORROW
            tokens.append(Token(TokenType.WHEN, WhenKeyword(token, day)))
        if token == "at":
            hour, minute = (int(x.strip()) for x in raw_tokens[index + 1].split(":"))
            time = Time(hour, minute)
            tokens.append(Token(TokenType.AT, AtKeyword(token, time)))
        if token == "do":
            description = " ".join(raw_tokens[index + 1 :])
            tokens.append(Token(TokenType.DO, DoKeyword(token, description)))
            break

    await ctx.respond(f"```py\n{pprint.pformat(tokens)}```")


@tanjun.as_loader
def load_module(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_module(client: tanjun.abc.Client) -> None:
    client.remove_component_by_name(component.name)
