from typing import TypedDict

from .snowflake import Snowflake
from .user import User


class _MemberOptional(TypedDict, total=False):
    user: User
    pending: bool
    permissions: str
    nick: str | None
    avatar: str | None
    premium_since: int | None
    communication_disabled_until: int | None


class Member(_MemberOptional):
    roles: list[Snowflake]
    joined_at: str
    deaf: bool
    mute: bool
