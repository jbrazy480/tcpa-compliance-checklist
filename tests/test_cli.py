import json
import os
from pathlib import Path
import subprocess
import sys
import pytest
from tcpa_toolkit.cli import main

ROOT=Path(__file__).resolve().parents[1]


@pytest.mark.parametrize('args,code,key', [
    (['window','+12125550100','--at','2026-09-26T14:00:00Z'],0,'allowed'),
    (['window','+12125550100','--at','2026-09-26T04:00:00Z'],1,'allowed'),
    (['next','+14155550101','--at','2026-09-26T12:00:00Z'],0,'next_allowed_time'),
    (['next','+19995550100','--at','2026-09-26T12:00:00Z'],1,'next_allowed_time'),
    (['consent-validate',str(ROOT/'examples/consent.jsonl')],0,'valid'),
    (['checklist',str(ROOT/'examples/status.yaml')],0,'items'),
])
def test_subcommands(args,code,key,tmp_path):
    p=subprocess.run([sys.executable,'-m','tcpa_toolkit',*args],cwd=tmp_path,text=True,capture_output=True)
    assert p.returncode==code,p.stderr
    assert key in json.loads(p.stdout)


@pytest.mark.parametrize('args', [
    ['window','bad','--at','2026-09-26T14:00:00Z'],
    ['window','+12125550100','--at','2026-09-26T14:00:00'],
    ['consent-validate','missing.jsonl'],
])
def test_handled_errors(args,capsys):
    assert main(args)==2
    captured=capsys.readouterr()
    assert 'error' in json.loads(captured.err) and not captured.out


def test_console_script():
    executable=Path(sys.executable).parent/'tcpa-check'
    p=subprocess.run([str(executable),'--help'],text=True,capture_output=True)
    assert p.returncode==0 and 'consent-validate' in p.stdout


def test_cli_scrub(tmp_path,capsys):
    assert main(['scrub',str(ROOT/'examples/leads.csv'),str(tmp_path/'out'), '--dnc',str(ROOT/'examples/internal_dnc.txt')])==0
    assert json.loads(capsys.readouterr().out)['removed_count']==2


def test_cli_invalid_consent(tmp_path,capsys):
    p=tmp_path/'bad'; p.write_text('{}\n')
    assert main(['consent-validate',str(p)])==1
    assert not json.loads(capsys.readouterr().out)['valid']
