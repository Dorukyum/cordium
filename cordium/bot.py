import asyncio
from asyncio.events import get_event_loop

from aiohttp import ClientSession

from .gateway import Gateway
from .http import HTTPClient

__all__ = ("Bot",)


class Bot(Gateway):
    def __init__(self, *, intents: int = 0) -> None:
        super().__init__(intents=intents)
        self.http = HTTPClient(self, loop=get_event_loop())

    def start(self, token: str | None = None) -> None:
        token = getattr(self, "token", token)
        if not token:
            raise Exception("no bot token set")
        self.token = token

        asyncio.run(self.setup())

    async def setup(self):
        self.session = ClientSession(
            headers={"Authorization": f"Bot {self.token}"},
        )

        try:
            await self.connect()
        except KeyboardInterrupt:
            await self.close()
        except Exception as e:
            raise e

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
        await self.dispatch(name, data)
