from __future__ import annotations

from typing import TYPE_CHECKING

from .message import Message
from .object import Object

if TYPE_CHECKING:
    from .bot import Bot

__all__ = ("State",)


class State:
    bot: Bot

    channels = {}
    guilds = {}
    members = {}
    messages = {}

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    async def create_message(self, data) -> Message:
        message = Message(self, channel=data["channel_id"], data=data)
        self.messages[message.id] = message
        return message

    async def process_event(self, name: str, data) -> None:
        name = name.lower()
        await self.bot.dispatch(f"raw_{name}", data)
        try:
            func = getattr(self, f"process_{name}")
        except AttributeError:
            pass
        else:
            await func(data)

    async def process_ready(self, data) -> None:
        for guild in data["guilds"]:
            self.guilds[guild["id"]] = Object(guild["id"])
        await self.bot.dispatch("ready")

    async def process_guild_create(self, data) -> None:
        ...

    async def process_message_create(self, data) -> None:
        message = await self.create_message(data)
        await self.bot.dispatch("message_create", message)
