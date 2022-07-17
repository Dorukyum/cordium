from typing import TypedDict

from .snowflake import Snowflake
from .user import User


class _MemberOptional(TypedDict, total=False):
    user: User
    nick: str
    avatar: str
    premium_since: int
    pending: bool
    permissions: str
    communication_disabled_until: int


class Member(_MemberOptional):
    roles: list[Snowflake]
    joined_at: int
    deaf: bool
    mute: bool
