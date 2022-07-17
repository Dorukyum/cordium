from typing import Literal, TypedDict

from .channel import Channel, ChannelMention
from .embed import Embed
from .message import Message
from .reaction import Reaction
from .snowflake import Snowflake
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


class _MessageOptional(TypedDict, total=False):
    reactions: list[Reaction]
    nonce: int | str
    webhook_id: Snowflake
    activity: MessageActivity
    application: PartialApplication
    application_id: Snowflake
    message_reference: MessageReference
    flags: int
    referenced_message: Message
    interaction: MessageInteraction
    thread: Channel
    components: list[MessageComponent]
    sticker_items: list[StickerItem]
    stickers: list[Sticker]


class Message(_MessageOptional):
    id: Snowflake
    channel_id: Snowflake
    author: User
    content: str
    timestamp: int
    edited_timestamp: int
    tts: bool
    mention_everyone: bool
    mentions: list[Snowflake]
    mention_roles: list[Snowflake]
    mention_channels: list[ChannelMention]
    attachments: list[Attachment]
    embeds: list[Embed]
    pinned: bool
    type: MessageType
