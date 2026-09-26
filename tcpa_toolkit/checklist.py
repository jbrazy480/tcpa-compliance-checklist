"""Render tracked checklist progress from a YAML id-to-status mapping."""
from importlib.resources import files
from pathlib import Path
import yaml


def checklist_progress(status_file: str | Path) -> dict:
    checklist = yaml.safe_load(files('tcpa_toolkit').joinpath('data/checklist.yaml').read_text())
    statuses = yaml.safe_load(Path(status_file).read_text())
    items = [item for group in checklist['groups'] for item in group['items']]
    ids = {item['id'] for item in items}
    if not isinstance(statuses, dict) or set(statuses) - ids:
        raise ValueError('status file must map known checklist ids to statuses')
    if any(s not in ('todo', 'done', 'not_applicable') for s in statuses.values()):
        raise ValueError('statuses must be todo, done or not_applicable')
    rows = [{**item, 'status': statuses.get(item['id'], 'todo')} for item in items]
    return {'done': sum(r['status'] == 'done' for r in rows), 'total': len(rows), 'items': rows}
