"""Execute the offline demo and expose captured output to the GIF renderer."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
COMMANDS = [
    ['window', '+12125550100', '--at', '2026-09-26T14:00:00Z'],
    ['next', '+14155550101', '--at', '2026-09-26T12:00:00Z'],
    ['scrub', 'examples/leads.csv', 'data/clean.csv', '--dnc', 'examples/internal_dnc.txt'],
    ['consent-validate', 'examples/consent.jsonl'],
    ['checklist', 'examples/status.yaml'],
]


def run_demo() -> list[tuple[str, str]]:
    (ROOT / 'data').mkdir(exist_ok=True)
    frames = []
    for args in COMMANDS:
        result = subprocess.run([sys.executable, '-m', 'tcpa_toolkit', *args],
                                cwd=ROOT, text=True, capture_output=True, check=True)
        frames.append(('tcpa-check ' + ' '.join(args), result.stdout))
    return frames


if __name__ == '__main__':
    for command, output in run_demo():
        print('$ ' + command)
        print(output)
