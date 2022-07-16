from asyncio import AbstractEventLoop

from .types import JSON, Snowflake

__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, bot, loop: AbstractEventLoop) -> None:
        self.bot = bot
        self.loop = loop

    async def request(self, method: str, path: str, data=None) -> JSON:
        data = data or {}
        response = await self.bot.session.request(
            method=method,
            url=f"https://discord.com/api/v10{path}",
            data=data,
        )
        if 300 >= response.status >= 200:
            if response.content_type == "application/json":
                return await response.json()
        raise Exception(response.status)

    async def get_me(self):
        return await self.request("GET", "/users/@me")

    async def send_message(self, channel_id: Snowflake, data) -> JSON:
        return await self.request("POST", f"/channels/{channel_id}/messages", data)

    async def create_application_command(self):
        await self.request("POST", f"/applications/813078122710827048/commands")

    async def respond_to_interaction(
        self, interaction_id: Snowflake, interaction_token: str, data
    ) -> JSON:
        return await self.request(
            "POST", f"/interactions/{interaction_id}/{interaction_token}/callback", data
        )
