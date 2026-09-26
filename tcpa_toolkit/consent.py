"""Validate evidence-record structure, not legal sufficiency or permission to dial."""
import json
import re
from urllib.parse import urlsplit
from datetime import datetime
from importlib.resources import files
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker


FORMATS = FormatChecker()


@FORMATS.checks("date-time", raises=(ValueError, OverflowError))
def _date_time(value: object) -> bool:
    # jsonschema's optional date-time extra is not a runtime dependency.
    if not isinstance(value, str):
        return True
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:[Zz]|[+-][0-9]{2}:[0-9]{2})", value):
        return False
    stamp = datetime.fromisoformat(value.upper().replace('Z', '+00:00'))
    if value[-6:-5] in ('+', '-'):
        if int(value[-5:-3]) > 23 or int(value[-2:]) > 59:
            return False
    return stamp.utcoffset() is not None


@FORMATS.checks("uri", raises=ValueError)
def _source_url(value: object) -> bool:
    # The source_url field intentionally accepts only absolute HTTP(S) URLs.
    if not isinstance(value, str):
        return True
    if any(char.isspace() or ord(char) < 32 for char in value):
        return False
    if re.search(r"%(?![0-9a-fA-F]{2})", value):
        return False
    parsed = urlsplit(value)
    return parsed.scheme in ('http', 'https') and bool(parsed.hostname) and parsed.port != 0


def validate_consent_log(path: str | Path) -> dict:
    schema = json.loads(files("tcpa_toolkit").joinpath("data/consent_log.schema.json").read_text())
    validator = Draft202012Validator(schema, format_checker=FORMATS)
    errors, records = [], 0
    with Path(path).open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            records += 1
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                errors.append({"line": line_no, "field": "", "message": "invalid JSON"})
                continue
            issues = list(validator.iter_errors(record))
            for issue in issues:
                # Avoid emitting disclosure text, IP addresses or phone values.
                errors.append({"line": line_no, "field": ".".join(map(str, issue.absolute_path)),
                               "message": f"failed {issue.validator} validation"})
            if not issues and record.get("revoked_at"):
                if datetime.fromisoformat(record['revoked_at'].upper().replace('Z','+00:00')) < datetime.fromisoformat(record['timestamp'].upper().replace('Z','+00:00')):
                    errors.append({"line": line_no, "field": "revoked_at", "message": "revocation precedes consent"})
    if not records:
        errors.append({"line": 0, "field": "", "message": "empty consent log"})
    return {"valid": not errors, "records": records, "errors": errors}
