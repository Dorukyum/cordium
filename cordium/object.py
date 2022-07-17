from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000


__all__ = ("Object",)


class Object:
    def __init__(self, id: int | str) -> None:
        self.id = int(id)

    @property
    def creation(self) -> datetime:
        timestamp = ((self.id >> 22) + DISCORD_EPOCH) / 1000
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
