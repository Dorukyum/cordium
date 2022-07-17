from asyncio import AbstractEventLoop
from typing import Any

from .message import Message
from .types.channel import Channel
from .types.component import MessageComponent
from .types.embed import Embed
from .types.emoji import Emoji
from .types.message import Attachment, MessageReference
from .types.snowflake import Snowflake
from .utils import MISSING

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
        headers = {"User-Agent": self.bot.user_agent}
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
            json=data,
            headers=headers,
        )
        if 300 >= response.status >= 200:
            if response.content_type == "application/json":
                return await response.json()
        raise Exception(response.status, response.reason)

    async def get_me(self):
        return await self.request("GET", "/users/@me")

    # channels
    async def get_channel(self, channel_id: Snowflake) -> Channel:
        return await self.request("PATCH", f"channels/{channel_id}")

    async def edit_channel(
        self, channel_id: Snowflake, data, *, reason: str | None = None
    ) -> Channel:
        return await self.request(
            "GET", f"channels/{channel_id}", data=data, reason=reason
        )

    async def delete_channel(
        self, channel_id: Snowflake, *, reason: str | None = None
    ) -> Channel:
        return await self.request("DELETE", f"channels/{channel_id}", reason=reason)

    # messages
    async def get_messages(
        self,
        channel_id: Snowflake,
        *,
        around: Snowflake | None = None,
        before: Snowflake | None = None,
        after: Snowflake | None = None,
        limit: int | None = None,
    ) -> list[Message]:
        data = {}
        if around is not None:
            data["around"] = around
        if before is not None:
            data["before"] = before
        if after is not None:
            data["after"] = after
        if limit is not None:
            data["v"] = limit
        return [
            Message(channel=d["channel_id"], data=d)
            for d in await self.request(
                "GET", f"/channels/{channel_id}/messages", data=data
            )
        ]

    async def get_message(
        self, channel_id: Snowflake, message_id: Snowflake
    ) -> Message:
        data = await self.request(
            "GET", f"/channels/{channel_id}/messages/{message_id}"
        )
        return Message(channel=data["channel_id"], data=data)

    async def send_message(
        self,
        channel_id: Snowflake,
        *,
        content: str | None = None,
        tts: bool | None = None,
        embeds: list[Embed] | None = None,
        allowed_mentions: Any = None,
        message_reference: MessageReference | None = None,
        components: list[MessageComponent] | None = None,
        sticker_ids: list[Snowflake] | None = None,
        files: Any | None = None,
        attachments: list[Attachment] | None = None,
        flags: int | None = None,
    ) -> Message:
        data = {}
        if content is not None:
            data["content"] = content
        if tts is not None:
            data["tts"] = tts
        if embeds is not None:
            data["embeds"] = embeds
        if allowed_mentions is not None:
            data["allowed_mentions"] = allowed_mentions
        if message_reference is not None:
            data["message_reference"] = message_reference
        if components is not None:
            data["components"] = components
        if sticker_ids is not None:
            data["sticker_ids"] = sticker_ids
        if files is not None:
            data["files"] = files
        if attachments is not None:
            data["attachments"] = attachments
        if flags is not None:
            data["flags"] = flags
        message = await self.request(
            "POST", f"/channels/{channel_id}/messages", data=data
        )
        return Message(channel=message["channel_id"], data=message)

    async def publish_message(
        self, channel_id: Snowflake, message_id: Snowflake
    ) -> Message:
        data = await self.request(
            "POST", f"/channels/{channel_id}/messages/{message_id}/crosspost"
        )
        return Message(channel=data["channel_id"], data=data)

    async def edit_message(
        self,
        channel_id: Snowflake,
        message_id: Snowflake,
        *,
        content: str = MISSING,
        embeds: list[Embed] = MISSING,
        allowed_mentions: Any = MISSING,
        components: list[MessageComponent] = MISSING,
        files: Any = MISSING,
        attachments: list[Attachment] = MISSING,
        flags: int = MISSING,
    ) -> Message:
        data = {}
        if content is not MISSING:
            data["content"] = content
        if embeds is not MISSING:
            data["embeds"] = embeds
        if allowed_mentions is not MISSING:
            data["allowed_mentions"] = allowed_mentions
        if components is not MISSING:
            data["components"] = components
        if files is not MISSING:
            data["files"] = files
        if attachments is not MISSING:
            data["attachments"] = attachments
        if flags is not MISSING:
            data["flags"] = flags
        message = await self.request(
            "PATCH", f"/channels/{channel_id}/messages/{message_id}", data=data
        )
        return Message(channel=message["channel_id"], data=message)

    async def delete_message(
        self, channel_id: Snowflake, message_id: Snowflake, *, reason: str | None = None
    ):
        return await self.request(
            "DELETE", f"/channels/{channel_id}/messages/{message_id}", reason=reason
        )

    async def bulk_delete_messages(
        self,
        channel_id: Snowflake,
        message_ids: list[Snowflake],
        *,
        reason: str | None = None,
    ):
        return await self.request(
            "PATCH",
            f"/channels/{channel_id}/messages/bulk-delete",
            data=message_ids,
            reason=reason,
        )

    # https://discord.com/developers/docs/resources/channel#edit-channel-permissions

    # emojis
    async def list_emojis(self, guild_id: Snowflake) -> list[Emoji]:
        return await self.request("GET", f"/guilds/{guild_id}/emojis")

    async def get_emoji(self, guild_id: Snowflake, emoji_id: Snowflake) -> Emoji:
        return await self.request("GET", f"/guilds/{guild_id}/emojis/{emoji_id}")

    async def create_emoji(
        self,
        guild_id: Snowflake,
        *,
        name: str,
        image: str,
        roles: list[Snowflake] | None = None,
        reason: str | None = None,
    ) -> Emoji:
        data: dict[str, str | list[Snowflake]] = {"name": name, "image": image}
        if roles is not None:
            data["roles"] = roles
        return await self.request(
            "POST", f"/guilds/{guild_id}/emojis", data=data, reason=reason
        )

    async def edit_emoji(
        self,
        guild_id: Snowflake,
        emoji_id: Snowflake,
        *,
        name: str | None = None,
        roles: list[Snowflake] | None = None,
        reason: str | None = None,
    ) -> Emoji:
        data = {}
        if name is not None:
            data["name"] = name
        if roles is not None:
            data["roles"] = roles
        return await self.request(
            "PATCH", f"/guilds/{guild_id}/emojis/{emoji_id}", data=data, reason=reason
        )

    async def delete_emoji(self, guild_id: Snowflake, emoji_id: Snowflake):
        return await self.request("DELETE", f"/guilds/{guild_id}/emojis/{emoji_id}")

    # interactions
    async def respond_to_interaction(
        self, interaction_id: Snowflake, interaction_token: str, data
    ):
        return await self.request(
            "POST",
            f"/interactions/{interaction_id}/{interaction_token}/callback",
            data=data,
        )
