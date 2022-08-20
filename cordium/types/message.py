from typing import Literal, TypedDict

from .application import Application
from .channel import Channel, ChannelMention
from .component import MessageComponent
from .embed import Embed
from .interaction import MessageInteraction
from .reaction import Reaction
from .snowflake import Snowflake
from .sticker import Sticker, StickerItem
from .user import User

MessageType = Literal[
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24
]
MessageActivityType = Literal[1, 2, 3, 5]


class MessageReference(TypedDict, total=False):
    message_id: Snowflake
    channel_id: Snowflake
    guild_id: Snowflake
    fail_if_not_exists: bool


class _MessageActivityOptional(TypedDict, total=False):
    party_id: str


class MessageActivity(_MessageActivityOptional):
    type: MessageActivityType


class _AttachmentOptional(TypedDict, total=False):
    description: str
    content_type: str
    height: int
    width: int
    ephemeral: bool


class Attachment(_AttachmentOptional):
    id: int
    filename: str
    size: int
    url: str
    proxy_url: str


class _MessageOptional(TypedDict, total=False):
    reactions: list[Reaction]
    nonce: int | str
    webhook_id: Snowflake
    activity: MessageActivity
    application: Application
    application_id: Snowflake
    message_reference: MessageReference
    flags: int
    interaction: MessageInteraction
    thread: Channel
    components: list[MessageComponent]
    sticker_items: list[StickerItem]
    stickers: list[Sticker]
    referenced_message: "Message" | None


class Message(_MessageOptional):
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: str
    tts: bool
    mention_everyone: bool
    mentions: list[Snowflake]
    mention_roles: list[Snowflake]
    mention_channels: list[ChannelMention]
    attachments: list[Attachment]
    embeds: list[Embed]
    pinned: bool
    type: MessageType
    edited_timestamp: str | None
