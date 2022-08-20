from typing import Literal, TypedDict

from .snowflake import Snowflake
from .user import User

StickerType = Literal[1, 2]
StickerFormatType = Literal[1, 2, 3]


class _StickerOptional(TypedDict, total=False):
    pack_id: Snowflake
    asset: Literal[""]
    available: bool
    guild_id: Snowflake
    user: User
    sort_value: int


class Sticker(_StickerOptional):
    id: Snowflake
    name: str
    tags: str
    type: StickerType
    format_type: StickerFormatType
    description: str | None


class StickerItem(TypedDict):
    id: Snowflake
    name: str
    format_type: StickerFormatType
