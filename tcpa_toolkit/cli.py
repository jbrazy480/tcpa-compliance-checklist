"""JSON output for automation; exit 1 means a blocked or invalid check."""
import argparse
import csv
from dataclasses import asdict
from datetime import datetime
import json
import sys
import yaml
from .calling_window import is_callable, next_allowed_time
from .consent import validate_consent_log
from .dnc import scrub_csv
from .checklist import checklist_progress


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog='tcpa-check')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('window', 'next'):
        p = sub.add_parser(name)
        p.add_argument('phone')
        p.add_argument('--at', required=True, help='ISO timestamp with UTC offset')
        p.add_argument('--start', default='08:00')
        p.add_argument('--end', default='21:00')
        p.add_argument('--tz-override')
    p = sub.add_parser('scrub')
    p.add_argument('input')
    p.add_argument('output')
    p.add_argument('--dnc', nargs='+', required=True)
    p.add_argument('--phone-column', default='phone')
    p = sub.add_parser('consent-validate')
    p.add_argument('path')
    p = sub.add_parser('checklist')
    p.add_argument('status_file')
    args = parser.parse_args(argv)
    code = 0
    try:
        if args.command in ('window', 'next'):
            at = datetime.fromisoformat(args.at.replace('Z', '+00:00'))
            options = dict(start=args.start, end=args.end, tz_override=args.tz_override)
            result = is_callable(args.phone, at, **options)
            if args.command == 'window':
                output = asdict(result)
                code = 0 if result.allowed else 1
            else:
                nxt = next_allowed_time(args.phone, at, **options)
                output = {'next_allowed_time': nxt.isoformat() if nxt else None,
                          'reason': 'next window found' if nxt else (result.reason if not result.local_times else 'no intersection within 370 days')}
                code = 0 if nxt else 1
        elif args.command == 'scrub':
            output = scrub_csv(args.input, args.output, args.dnc, args.phone_column)
        elif args.command == 'consent-validate':
            output = validate_consent_log(args.path)
            code = 0 if output['valid'] else 1
        else:
            output = checklist_progress(args.status_file)
        print(json.dumps(output, indent=2))
        return code
    except (ValueError, OSError, yaml.YAMLError, csv.Error) as exc:
        print(json.dumps({'error': str(exc)}), file=sys.stderr)
        return 2
