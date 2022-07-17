from typing import TypedDict

from .emoji import Emoji


class Reaction(TypedDict):
    count: int
    me: bool
    emoji: Emoji
