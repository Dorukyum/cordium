from typing import Any


def try_snowflake(data, key: str) -> int | None:
    try:
        snowflake = data[key]
    except KeyError:
        return None
    return snowflake is not None and int(snowflake)


class _MISSING:
    """Represents a "missing" argument, not to be confused with `None`."""


MISSING: Any = _MISSING()
