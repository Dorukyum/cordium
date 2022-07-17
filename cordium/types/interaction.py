from typing import Literal, TypedDict

from .member import Member
from .snowflake import Snowflake
from .user import User

InteractionType = Literal[1, 2, 3, 4, 5]


class _MessageInteractionOptional(TypedDict, total=False):
    member: Member


class MessageInteraction(_MessageInteractionOptional):
    id: Snowflake
    type: InteractionType
    name: str
    user: User
