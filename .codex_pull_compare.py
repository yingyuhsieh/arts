import pathlib
import shutil
import subprocess
import sys

root = pathlib.Path(__file__).parent
backup = root / '.local_pull_backup'

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

incoming = set(git('diff', '--name-only', '-z', 'HEAD..origin/main').decode('utf-8').rstrip('\0').split('\0'))
untracked = set(git('ls-files', '--others', '--exclude-standard', '-z').decode('utf-8').rstrip('\0').split('\0'))
overlap = sorted(incoming & untracked)
modified = set(git('diff', '--name-only', '-z').decode('utf-8').rstrip('\0').split('\0'))
tracked_overlap = sorted(incoming & modified)
if backup.exists():
    raise RuntimeError(f'Backup already exists: {backup}')
backup.mkdir()
result = None
try:
    for name in overlap:
        source = root / name
        destination = backup / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(source, destination)
    for name in tracked_overlap:
        source = root / name
        destination = backup / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        subprocess.check_call(['git', '-C', str(root), 'restore', '--worktree', '--', name])
    print(f'Preserved {len(overlap)} untracked and {len(tracked_overlap)} edited files', flush=True)
    result = subprocess.run(['git', '-C', str(root), 'pull', '--ff-only'])
    if result.returncode:
        print(f'Pull failed ({result.returncode}); restoring local files', flush=True)
finally:
    for name in overlap + tracked_overlap:
        source = backup / name
        if source.exists():
            destination = root / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(source, destination)
    if backup.exists():
        shutil.rmtree(backup)
if result.returncode:
    sys.exit(result.returncode)
print(f'Restored {len(overlap) + len(tracked_overlap)} local files over the pulled versions', flush=True)
