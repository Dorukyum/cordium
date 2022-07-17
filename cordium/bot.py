from asyncio import get_event_loop

from aiohttp import ClientSession

from .gateway import Gateway
from .http import HTTPClient
from .state import State

__all__ = ("Bot",)


class Bot(Gateway):
    user_agent = "DiscordBot (https://github.com/Dorukyum/cordium, 1.0.0)"

    def __init__(self, *, intents: int = 0) -> None:
        super().__init__(intents=intents)
        self.state = State(self)
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

    async def dispatch(self, name: str, *args) -> None:
        try:
            func = getattr(self, f"on_{name.lower()}")
        except AttributeError:
            pass
        else:
            await func(*args)
