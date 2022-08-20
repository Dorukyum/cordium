from typing import TypedDict

from .snowflake import Snowflake


class _UserOptional(TypedDict, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    locale: str
    verified: bool
    flags: int
    premium_type: int
    public_flag: int
    accent_color: int | None
    banner: str | None
    email: str | None


class User(_UserOptional, TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: str | None
