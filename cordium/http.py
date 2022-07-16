from asyncio import AbstractEventLoop
from typing import Any

from .types.channel import Channel
from .types.snowflake import Snowflake
from .types.message import Message

__all__ = ("HTTPClient",)


class HTTPClient:
    def __init__(self, bot, loop: AbstractEventLoop) -> None:
        self.bot = bot
        self.loop = loop

    async def request(
        self,
        method: str,
        path: str,
        *,
        data: dict[str, Any] | list[Snowflake] | list[dict[str, Any]] | None = None,
        reason: str | None = None,
        locale: str | None = None,
    ) -> Any:
        headers = {"User-Agent": ""}
        if reason is not None:
            headers["X-Audit-Log-Reason"] = reason
        if (token := self.bot.token) is not None:
            headers["Authorization"] = f"Bot {token}"
        if data is not None:
            headers["Content-Type"] = "application/json"
        if locale is not None:
            headers["X-Discord-Locale"] = locale

        response = await self.bot.session.request(
            method=method,
            url=f"https://discord.com/api/v10{path}",
            data=data,
            headers=headers,
        )
        if 300 >= response.status >= 200:
            if response.content_type == "application/json":
                return await response.json()
        raise Exception(response.status)

    async def get_me(self):
        return await self.request("GET", "/users/@me")

    # channels
    async def get_channel(self, channel_id: Snowflake) -> Channel:
        return await self.request("PATCH", f"channels/{channel_id}")

    async def edit_channel(self, channel_id: Snowflake, data, *, reason: str | None = None) -> Channel:
        return await self.request("GET", f"channels/{channel_id}", data=data, reason=reason)

    async def delete_channel(
        self, channel_id: Snowflake, *, reason: str | None = None
    ) -> Channel:
        return await self.request("DELETE", f"channels/{channel_id}", reason=reason)

    async def get_messages(self, channel_id: Snowflake) -> list[Message]:
        return await self.request("GET", f"/channels/{channel_id}/messages")

    async def get_message(self, channel_id: Snowflake, message_id: Snowflake) -> Message:
        return await self.request(
            "GET", f"/channels/{channel_id}/messages/{message_id}"
        )

    async def send_message(self, channel_id: Snowflake, data) -> Message:
        return await self.request("POST", f"/channels/{channel_id}/messages", data=data)

    async def publish_message(
        self, channel_id: Snowflake, message_id: Snowflake
    ) -> Message:
        return await self.request(
            "POST", f"/channels/{channel_id}/messages/{message_id}/crosspost"
        )

    async def edit_message(self, channel_id: Snowflake, message_id: Snowflake) -> Message:
        return await self.request("PATCH", f"/channels/{channel_id}/messages/{message_id}")

    async def delete_message(self, channel_id: Snowflake, message_id: Snowflake, *, reason: str | None = None):
        return await self.request("DELETE", f"/channels/{channel_id}/messages/{message_id}", reason=reason)

    async def bulk_delete_messages(self, channel_id: Snowflake, message_ids: list[Snowflake], *, reason: str | None = None):
        return await self.request("PATCH", f"/channels/{channel_id}/messages/bulk-delete", data=message_ids, reason=reason)

    # https://discord.com/developers/docs/resources/channel#edit-channel-permissions

    async def respond_to_interaction(
        self, interaction_id: Snowflake, interaction_token: str, data
    ):
        return await self.request(
            "POST",
            f"/interactions/{interaction_id}/{interaction_token}/callback",
            data=data,
        )
