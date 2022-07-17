from typing import TypedDict

from .snowflake import Snowflake
from .user import User


class _EmojiOptional(TypedDict, total=False):
    name: str  # can be None only in reaction emoji objects
    roles: list[Snowflake]
    user: User
    require_colons: bool
    managed: bool
    animated: bool
    available: bool


class Emoji(_EmojiOptional):
    id: Snowflake
