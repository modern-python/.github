import datetime
import json
import os
import typing
import urllib.request


ENDOFLIFE_URL: typing.Final = "https://endoflife.date/api/python.json"


def newest_cycle_from_payload(payload: list[dict[str, typing.Any]], today: datetime.date) -> str:
    released = [
        item["cycle"]
        for item in payload
        if isinstance(item.get("releaseDate"), str) and datetime.date.fromisoformat(item["releaseDate"]) <= today
    ]
    if not released:
        msg = "endoflife.date returned no released Python cycle"
        raise ValueError(msg)
    return max(released, key=lambda cycle: tuple(int(part) for part in cycle.split(".")))


def newest_cycle() -> str:
    if pinned := os.environ.get("CENSUS_NEWEST_PYTHON"):
        return pinned
    request = urllib.request.Request(ENDOFLIFE_URL, headers={"User-Agent": "modern-python-census"})
    with urllib.request.urlopen(request, timeout=30) as response:  # noqa: S310
        payload = json.loads(response.read())
    return newest_cycle_from_payload(payload, datetime.datetime.now(tz=datetime.UTC).date())
