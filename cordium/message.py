from __future__ import annotations

from typing import TYPE_CHECKING

from .object import Object
from .utils import try_snowflake

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
