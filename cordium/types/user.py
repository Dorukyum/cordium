from typing import TypedDict

from .snowflake import Snowflake


class _UserOptional(TypedDict, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    banner: str
    accent_color: int
    locale: str
    verified: bool
    email: str
    flags: int
    premium_type: int
    public_flag: int


class User(_UserOptional, TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: str
