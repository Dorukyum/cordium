import asyncio
from asyncio.events import get_event_loop

from aiohttp import ClientSession

from .gateway import Gateway
from .http import HTTPClient
from .message import Message

__all__ = ("Bot",)


class Bot(Gateway):
    user_agent = "DiscordBot (https://github.com/Dorukyum/cordium, 1.0.0)"

    def __init__(self, *, intents: int = 0) -> None:
        super().__init__(intents=intents)
        self.loop = get_event_loop()
        self.http = HTTPClient(self, loop=self.loop)

    def start(self, token: str | None = None) -> None:
        token = getattr(self, "token", token)
        if not token:
            raise Exception("no bot token set")
        self.token = token

        self.loop.run_until_complete(self.setup())
        self.loop.run_until_complete(self.connect())

    async def setup(self):
        self.session = ClientSession(
            headers={"Authorization": f"Bot {self.token}"},
        )

    async def dispatch(self, name: str, data=None) -> None:
        try:
            func = getattr(self, f"on_{name.lower()}")
            if data is not None:
                return await func(data)
            await func()
        except AttributeError:
            pass

    async def process_event(self, name: str, data) -> None:
        if name == "READY":
            return await self.dispatch("READY")
        if name == "MESSAGE_CREATE":
            message = Message(channel=data["channel_id"], data=data)
            return await self.dispatch("MESSAGE_CREATE", message)
        await self.dispatch(name, data)
