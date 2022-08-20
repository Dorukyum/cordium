from typing import Literal, TypedDict

from .snowflake import Snowflake
from .user import User

MembershipState = Literal[1, 2]


class TeamMember(TypedDict):
    membership_state: MembershipState
    permissions: list[str]
    team_id: Snowflake
    user: User


class Team(TypedDict):
    id: Snowflake
    members: list[TeamMember]
    name: str
    owner_user_id: Snowflake
    icon: str | None


class InstallParams(TypedDict):
    scopes: list[str]
    permissions: str


class _ApplicationOptional(TypedDict, total=False):
    owner: User
    rpc_origins: list[str]
    terms_of_service_url: str
    privacy_policy_url: str
    guild_id: Snowflake
    primary_sku_id: Snowflake
    slug: str
    cover_image: str
    flags: int
    tags: list[str]
    install_params: InstallParams
    custom_install_url: str


class Application(_ApplicationOptional):
    id: Snowflake
    name: str
    description: str
    bot_public: bool
    bot_require_code_grant: bool
    summary: Literal[""]
    verify_key: str
    team: Team | None
    icon: str | None
