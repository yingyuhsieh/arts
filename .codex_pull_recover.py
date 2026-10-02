import os
import pathlib
import shutil
import subprocess

root = pathlib.Path(__file__).parent
backup = root / '.local_pull_backup'
if not backup.is_dir():
    raise RuntimeError('Preserved local-file backup is missing')

def git(*args):
    return subprocess.check_output(['git', '-C', str(root), *args])

lock = root / '.git' / 'index.lock'
if lock.exists():
    lock.unlink()

incoming = set(git('diff', '--name-only', '-z', 'HEAD..origin/main').decode('utf-8').rstrip('\0').split('\0'))
tracked = set(git('ls-files', '-z').decode('utf-8').rstrip('\0').split('\0'))
preserved = [p for p in backup.rglob('*') if p.is_file()]
print(f'Backup has {len(preserved)} local files', flush=True)
for name in incoming - tracked:
    path = root / name
    if path.is_file():
        path.unlink()
for path in preserved:
    name = path.relative_to(backup).as_posix()
    if name in tracked:
        subprocess.check_call(['git', '-C', str(root), 'restore', '--worktree', '--', name])

env = os.environ.copy()
env['GIT_LFS_SKIP_SMUDGE'] = '1'
result = subprocess.run(['git', '-C', str(root), 'pull', '--ff-only'], env=env)
for source in preserved:
    destination = root / source.relative_to(backup)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
if result.returncode:
    raise RuntimeError(f'Pull failed ({result.returncode}); backup remains at {backup}')
shutil.rmtree(backup)
print(f'Restored {len(preserved)} local files', flush=True)
