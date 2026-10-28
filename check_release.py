"""Fail closed if a public release includes any file outside the reviewed list.

Run from the root of this standalone public repository before every commit/push.
This checks file selection and obvious identifiers; it is not a substitute for
reviewing the exact content and the data provider's publication terms.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ALLOWED = {
    '.gitignore', 'README.md', 'INPUTS.md', 'LICENSE', 'requirements.txt',
    'check_release.py', 'taste_odor_methods/__init__.py',
    'taste_odor_methods/episodes.py', 'taste_odor_methods/evaluation.py',
}
BLOCKED = re.compile(r'/Users/[^/\s]+|\b[0-9a-f]{64}\b', re.IGNORECASE)


def main():
    tracked = subprocess.check_output(
        ['git', '-C', str(ROOT), 'ls-files', '-z'], text=True
    ).split('\0')
    tracked = {name for name in tracked if name}
    files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob('*')
        if path.is_file() and '.git' not in path.relative_to(ROOT).parts
        and '__pycache__' not in path.relative_to(ROOT).parts
    }
    problems = []
    if files != ALLOWED:
        problems.append(f'Working files differ from allowlist: extra={sorted(files-ALLOWED)}, missing={sorted(ALLOWED-files)}')
    if tracked != ALLOWED:
        problems.append(f'Git staged/tracked paths differ from allowlist: extra={sorted(tracked-ALLOWED)}, missing={sorted(ALLOWED-tracked)}')
    for name in sorted(files & ALLOWED):
        path = ROOT / name
        if path.stat().st_size > 100_000:
            problems.append(f'{name}: exceeds 100 KB')
        try:
            body = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            problems.append(f'{name}: is not UTF-8 text')
            continue
        if name != 'check_release.py' and BLOCKED.search(body):
            problems.append(f'{name}: contains a blocked identifier, path, or 64-character hash')
    if problems:
        print('Release check FAILED:')
        print('\n'.join(problems))
        return 1
    print(f'Release check passed: exactly {len(ALLOWED)} reviewed, text-only files are tracked.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
