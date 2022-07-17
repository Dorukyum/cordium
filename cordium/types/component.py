from typing import Literal, TypedDict


ComponentType = Literal[1, 2, 3, 4]


class MessageComponent(TypedDict):
    type: ComponentType
