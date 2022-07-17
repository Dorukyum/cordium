from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .object import Object
from .utils import MISSING, try_snowflake

if TYPE_CHECKING:
    from .state import State
    from .types.component import MessageComponent
    from .types.embed import Embed
    from .types.message import Application as ApplicationData
    from .types.message import Attachment
    from .types.message import Message as MessageData
    from .types.message import MessageActivity as MessageActivityData
    from .types.message import MessageType
    from .types.reaction import Reaction
    from .types.sticker import StickerItem

__all__ = ("Message",)


class Message(Object):
    def __init__(self, state: State, *, channel, data: MessageData) -> None:
        self.state = state
        self.id: int = int(data["id"])
        self.channel_id = data["channel_id"]
        self.content: str = data["content"]
        self.pinned: bool = data["pinned"]
        self.tts: bool = data["tts"]
        self.mention_everyone: bool = data["mention_everyone"]
        self.flags: int = data.get("flags", 0)
        self.type: MessageType = data["type"]
        self.nonce: int | str | None = data.get("nonce")
        self.webhook_id: int | None = try_snowflake(data, "webhook_id")
        self.application: ApplicationData | None = data.get("application")
        self.activity: MessageActivityData | None = data.get("activity")

        # TODO: convert to corresponding objects
        self.channel = channel
        self.attachments: list[Attachment] = data["attachments"]
        self.embeds: list[Embed] = data["embeds"]
        self.last_edited: str = data["edited_timestamp"]
        self.reactions: list[Reaction] = data.get("reactions", [])
        self.stickers: list[StickerItem] = data.get("sticker_items", [])
        self.components: list[MessageComponent] = data.get("components", [])

    async def edit(
        self,
        *,
        content: str = MISSING,
        embeds: list[Embed] = MISSING,
        allowed_mentions: Any = MISSING,
        components: list[MessageComponent] = MISSING,
        files: Any = MISSING,
        attachments: list[Attachment] = MISSING,
        flags: int = MISSING,
    ) -> Message:
        """Edits the message and returns the updated message."""
        return await self.state.bot.http.edit_message(
            self.channel_id,
            self.id,
            content=content,
            embeds=embeds,
            allowed_mentions=allowed_mentions,
            components=components,
            files=files,
            attachments=attachments,
            flags=flags,
        )

    async def publish(self) -> Message:
        """ "Publishes" (or "crossposts") the message."""
        return await self.state.bot.http.publish_message(self.channel_id, self.id)

    async def delete(self, reason: str | None = None) -> Message:
        """Deletes the message and returns the deleted message."""
        return await self.state.bot.http.delete_message(
            self.channel_id, self.id, reason=reason
        )
