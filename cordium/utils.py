def try_snowflake(data, key: str) -> int | None:
    try:
        snowflake = data[key]
    except KeyError:
        return None
    return snowflake is not None and int(snowflake)
