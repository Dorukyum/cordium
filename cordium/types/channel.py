from typing import Literal, TypedDict

from .snowflake import Snowflake
from .user import User

ChannelType = Literal[0, 1, 2, 3, 4, 5, 10, 11, 12, 13]
AutoArchiveDuration = Literal[60, 1440, 4320, 10080]


class ChannelMention(TypedDict):
    id: Snowflake
    guild_id: Snowflake
    type: ChannelType
    name: str


class PermissionOverwrite(TypedDict):
    id: Snowflake
    type: Literal[0, 1]
    allow: str
    deny: str


class _ThreadMetadataOptional(TypedDict, total=False):
    invitable: bool
    create_timestamp: str


class ThreadMetadata(_ThreadMetadataOptional):
    archived: bool
    auto_archive_duration: AutoArchiveDuration
    archive_timestamp: str
    locked: bool


class _ThreadMemberOptional(TypedDict, total=False):
    id: Snowflake
    user_id: Snowflake


class ThreadMember(_ThreadMemberOptional):
    join_timestamp: str
    flags: int


class _ChannelOptional(TypedDict, total=False):
    guild_id: Snowflake
    position: int
    permission_overwrites: list[PermissionOverwrite]
    nsfw: bool
    bitrate: int
    user_limit: int
    rate_limit_per_user: int
    recipients: list[User]
    owner_id: Snowflake
    application_id: Snowflake
    video_quality_mode: int
    message_count: int
    member_count: int
    thread_metadata: ThreadMetadata
    member: ThreadMember
    default_auto_archive_duration: AutoArchiveDuration
    permissions: str
    flags: int
    name: str | None
    topic: str | None
    last_message_id: Snowflake | None
    icon: str | None
    parent_id: Snowflake | None
    last_pin_timestamp: str | None
    rtc_region: str | None


class Channel(_ChannelOptional):
    id: Snowflake
    type: ChannelType
