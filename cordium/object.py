from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000


__all__ = ("Object",)


class Object:
    def __init__(self, id: int | str) -> None:
        self.id = int(id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.id == other.id

    def __ne__(self, other: object) -> bool:
        return (not isinstance(other, self.__class__)) or self.id != other.id

    @property
    def creation(self) -> datetime:
        timestamp = ((self.id >> 22) + DISCORD_EPOCH) / 1000
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
