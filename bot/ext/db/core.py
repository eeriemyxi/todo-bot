import logging
import typing as t
from enum import Enum
from pathlib import Path

import aiofile
import aiosqlite

logger = logging.getLogger(__name__)

HookListType: t.TypeAlias = list[tuple[t.Callable[..., t.Awaitable], tuple[t.Any, ...]]]


class HookType(Enum):
    BEFORE_CONN = 1
    AFTER_CONN = 2


class BaseDatabase:
    SCRIPT_PATH = Path("bot/ext/db/scripts")
    SCRIPT_NAMES = ("setup.sql",)

    def __init__(self):
        self._conn: aiosqlite.Connection | None = None
        self.before_hooks: HookListType = []
        self.after_hooks: HookListType = [(self.load_scripts, ())]

    async def connect(self) -> None:
        await self.call_hooks(HookType.BEFORE_CONN)
        self._conn = await aiosqlite.connect(".base_database.db")
        await self.call_hooks(HookType.AFTER_CONN)

    async def call_hooks(
        self, hook_type: HookType, *, hook_name: str | None = None
    ) -> None:
        match hook_type:
            case HookType.BEFORE_CONN:
                hooks = self.before_hooks
            case HookType.AFTER_CONN:
                hooks = self.after_hooks

        for hook, args in hooks:
            logger.info(
                "Calling hook `%s` on `%s` with type `%s`.",
                hook.__name__,
                self.__class__.__name__,
                hook_type.name,
            )
            if hook_name:
                if hook.__name__ == hook_name:
                    await hook(*args)
                    return
            else:
                await hook(*args)

    async def load_scripts(self) -> None:
        for file in self.SCRIPT_PATH.glob("*.sql"):
            if file.name in self.SCRIPT_NAMES and self._conn:
                async with aiofile.async_open(file, "r") as file_buf:
                    logger.info(
                        "Executing script `%s` on `%s`",
                        file.name,
                        self.__class__.__name__,
                    )
                    await self._conn.executescript(await file_buf.read())
