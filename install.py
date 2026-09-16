"""Install a self-contained ZhangLuo skill. Standard library only; no downloads."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def default_destination(agent):
    if agent == 'codex':
        return Path.home() / '.agents' / 'skills' / 'zhangluo'
    if agent == 'codex-legacy':
        return Path(os.environ.get('CODEX_HOME', str(Path.home()/'.codex'))) / 'skills' / 'zhangluo'
    if agent == 'claude':
        return Path.home() / '.claude' / 'skills' / 'zhangluo'
    raise ValueError('For other agents, provide --destination with the full skill directory.')

def package_files():
    entries = json.loads((ROOT/'PACKAGE_FILES.json').read_text(encoding='utf-8'))['files']
    for entry in entries:
        rel = Path(entry['path'])
        source = (ROOT/rel).resolve()
        if rel.is_absolute() or '..' in rel.parts or not source.is_relative_to(ROOT):
            raise ValueError('Invalid package path: ' + str(rel))
        if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != entry['sha256']:
            raise ValueError('Missing or modified package file: ' + str(rel))
    return [entry['path'] for entry in entries] + ['PACKAGE_FILES.json']

def install(destination):
    dest = Path(destination).expanduser().resolve()
    if dest == ROOT or dest.is_relative_to(ROOT) or ROOT.is_relative_to(dest):
        raise ValueError('Choose a destination separate from the source repository.')
    files = package_files()
    if dest.exists():
        actual = {p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}
        if actual == set(files) and all((dest/f).read_bytes() == (ROOT/f).read_bytes() for f in files):
            status = 'already_installed'
        else:
            raise ValueError('Destination exists with different contents; it was not changed. Choose --destination with a new directory name.')
    else:
        # mkdir without exist_ok protects against concurrent installs.
        dest.mkdir(parents=True, exist_ok=False)
        for name in files:
            target=dest/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT/name,target)
        status = 'installed'
    check=subprocess.run([sys.executable,'-X','utf8',str(dest/'zhangluo.py'),'doctor'],capture_output=True,text=True,encoding='utf-8')
    if check.returncode:
        raise ValueError('Installed files did not pass doctor: '+check.stderr)
    return {'status':status,'destination':str(dest),'version':(ROOT/'VERSION').read_text().strip(),
            'doctor':json.loads(check.stdout),'next_step':'Reload skills or start a new agent session; then use zhangluo.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--agent',choices=['codex','codex-legacy','claude','generic'],default='codex')
    p.add_argument('--destination',help='Full destination directory including the skill name')
    p.add_argument('--check',action='store_true',help='Check packaged files without installing')
    a=p.parse_args()
    try:
        if a.check:
            print(json.dumps({'success':True,'files_checked':len(package_files())}))
        else:
            print(json.dumps(install(a.destination or default_destination(a.agent)),ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError) as exc:
        print(str(exc),file=sys.stderr)
        return 1
if __name__=='__main__':
    raise SystemExit(main())
