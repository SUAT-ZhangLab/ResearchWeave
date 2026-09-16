"""ResearchWeave: research records and iterative program evaluation."""
import runpy
import sys
from pathlib import Path

def main():
    if sys.version_info < (3, 10):
        raise SystemExit('Python 3.10+ is required; Python 3.12 is recommended.')
    root = Path(__file__).resolve().parent
    if len(sys.argv) == 2 and sys.argv[1] == '--version':
        print((root / 'VERSION').read_text().strip())
        return
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '--help'):
        print('Usage: python researchweave.py {doctor|research|era} [arguments]')
        print('Research: init, record, status, report, run, doctor')
        print('ERA: init, ask, tell, status, finalize')
        return
    if sys.argv[1] == 'doctor':
        engine = 'research'
    elif sys.argv[1] in ('research', 'era'):
        engine = sys.argv.pop(1)
    else:
        raise SystemExit('Unknown engine. Run python researchweave.py --help')
    script = root / 'scripts' / (engine + '.py')
    sys.path.insert(0, str(script.parent))
    sys.argv[0] = str(script)
    runpy.run_path(str(script), run_name='__main__')

if __name__ == '__main__':
    main()
