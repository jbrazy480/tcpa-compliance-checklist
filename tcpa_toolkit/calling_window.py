"""Conservative local-time windows, with UTC traversal through DST changes."""
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from functools import lru_cache
from importlib.resources import files
import json
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from .phones import require_e164


@dataclass(frozen=True)
class WindowResult:
    allowed: bool
    local_times: dict[str, str]
    reason: str


@lru_cache(maxsize=1)
def timezone_map() -> dict[str, list[str]]:
    return json.loads(files("tcpa_toolkit").joinpath("data/npa_timezones.json").read_text())


def _clock(value: str) -> time:
    if not re.fullmatch(r"[0-2][0-9]:[0-5][0-9]", value):
        raise ValueError("window must use HH:MM")
    return time.fromisoformat(value)


def _setup(phone: str, at: datetime, start: str, end: str, override: str | None):
    require_e164(phone)
    if at.tzinfo is None or at.utcoffset() is None:
        raise ValueError("at_utc must be timezone-aware")
    lower, upper = _clock(start), _clock(end)
    if not time(8) <= lower < upper <= time(21):
        raise ValueError("window must be within 08:00-21:00, with start before end")
    names = [override] if override else timezone_map().get(phone[2:5], [])
    try:
        zones = [ZoneInfo(name) for name in names]
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise ValueError("unknown tz_override") from exc
    return at.astimezone(timezone.utc), lower, upper, zones


def is_callable(phone_e164: str, at_utc: datetime, start: str = "08:00",
                end: str = "21:00", tz_override: str | None = None) -> WindowResult:
    """Check [start, end) in every candidate zone. Invalid inputs raise ValueError."""
    at, lower, upper, zones = _setup(phone_e164, at_utc, start, end, tz_override)
    if not zones:
        return WindowResult(False, {}, "unknown timezone, supply tz_override")
    local = {z.key: at.astimezone(z) for z in zones}
    allowed = all(lower <= dt.time() < upper for dt in local.values())
    return WindowResult(allowed, {z: dt.isoformat() for z, dt in local.items()},
                        "within all local windows" if allowed else "outside one or more local windows")


def next_allowed_time(phone_e164: str, at_utc: datetime, start: str = "08:00",
                      end: str = "21:00", tz_override: str | None = None) -> datetime | None:
    """Return earliest allowed UTC instant at or after input, or None within 370 days.

    Minute boundaries suffice for modern US/Canada zones and HH:MM windows.
    The original instant is preserved when already allowed. UTC iteration avoids
    nonexistent or repeated local wall-time construction during DST changes.
    """
    at, lower, upper, zones = _setup(phone_e164, at_utc, start, end, tz_override)
    if not zones:
        return None
    def allowed(moment: datetime) -> bool:
        return all(lower <= moment.astimezone(z).time() < upper for z in zones)
    if allowed(at):
        return at
    candidate = at.replace(second=0, microsecond=0) + timedelta(minutes=1)
    limit = at + timedelta(days=370)
    while candidate <= limit:
        if allowed(candidate):
            return candidate
        candidate += timedelta(minutes=1)
    return None
