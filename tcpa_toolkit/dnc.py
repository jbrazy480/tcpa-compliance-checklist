"""Internal-list scrubbing only. Never queries the National DNC Registry."""
import csv
from pathlib import Path
from .phones import normalize_phone


def load_dnc(paths: list[str | Path]) -> set[str]:
    """Read one number per line, with blank lines and # comments allowed.

    Malformed entries abort instead of silently weakening suppression.
    """
    numbers = set()
    for path in paths:
        for line_no, line in enumerate(Path(path).read_text().splitlines(), 1):
            if line.strip() and not line.lstrip().startswith("#"):
                try:
                    numbers.add(normalize_phone(line.strip()))
                except ValueError as exc:
                    raise ValueError(f"{path}:{line_no}: invalid DNC number") from exc
    return numbers


def is_dnc(phone: str, numbers: set[str]) -> bool:
    return normalize_phone(phone) in numbers


def scrub_csv(input: str | Path, output: str | Path,
              dnc_files: list[str | Path], phone_column: str = "phone") -> dict:
    """Remove internal DNC matches and malformed phones; report CSV record numbers.

    Retained rows preserve original fields. The entire input is validated before
    writing. Reports contain row numbers, not phone numbers.
    """
    source, target = Path(input), Path(output)
    if source.resolve() == target.resolve() or any(target.resolve() == Path(p).resolve() for p in dnc_files):
        raise ValueError("output must differ from input and DNC files")
    blocked = load_dnc(dnc_files)
    kept, removed = [], []
    with source.open(newline="", encoding="utf-8-sig") as stream:
        reader = csv.DictReader(stream)
        fields = reader.fieldnames
        if not fields or phone_column not in fields or len(set(fields)) != len(fields):
            raise ValueError("missing phone column or duplicate CSV headers")
        for record, row in enumerate(reader, 2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f"malformed CSV record {record}")
            try:
                reason = "internal_dnc" if is_dnc(row[phone_column], blocked) else None
            except ValueError:
                reason = "invalid_phone"
            if reason:
                removed.append({"row": record, "reason": reason})
            else:
                kept.append(row)
    with target.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        writer.writerows(kept)
    return {"total": len(kept) + len(removed), "kept": len(kept),
            "removed_count": len(removed), "removed": removed,
            "scope": "internal lists only"}
