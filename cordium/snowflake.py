from datetime import datetime, timezone

DISCORD_EPOCH = 1420070400000


class Snowflake:
    def __init__(self, id: int | str, /) -> None:
        self.id = int(id)

    @property
    def creation(self) -> datetime:
        return datetime.fromtimestamp((self.id >> 22) + DISCORD_EPOCH, tz=timezone.utc)
