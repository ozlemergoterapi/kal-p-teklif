"""Ad-hoc sign relocated Mach-O files before putting them in the app bundle.

conda-pack --dest-prefix rewrites bytes without refreshing Mach-O signatures.
This is local integrity signing, not an Apple Developer ID or notarization.
"""
import subprocess
import sys
from pathlib import Path

MACHO = {bytes.fromhex(h) for h in ('feedface','cefaedfe','feedfacf','cffaedfe','cafebabe','bebafeca','cafebabf','bfbafeca')}

def sign_runtime(root):
    count = 0
    for file in sorted(Path(root).rglob('*')):
        if file.is_symlink() or not file.is_file() or file.suffix == '.class':
            continue
        with file.open('rb') as stream:
            magic = stream.read(4)
        if magic not in MACHO:
            continue
        subprocess.run(['/usr/bin/codesign','--force','--sign','-','--timestamp=none',str(file)],check=True,capture_output=True,text=True)
        subprocess.run(['/usr/bin/codesign','--verify','--strict',str(file)],check=True,capture_output=True,text=True)
        count += 1
    if not count:
        raise RuntimeError('No Mach-O runtime files found')
    print(f'Relocated runtime: {count} Mach-O signatures refreshed and verified.')

if __name__ == '__main__':
    if sys.platform != 'darwin':
        raise SystemExit('This build step requires macOS')
    try:
        sign_runtime(sys.argv[1])
    except subprocess.CalledProcessError as error:
        raise SystemExit(f'Runtime signing failed: {error.cmd[-1]}\n{error.stderr}')
