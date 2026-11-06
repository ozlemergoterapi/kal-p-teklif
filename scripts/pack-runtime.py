"""Run inside the native Windows/macOS conda build environment; never on customer PCs."""
import hashlib,json,os,platform,subprocess,sys,tarfile,tempfile,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
if sys.platform not in ['win32','darwin']:raise SystemExit('Windows ve Mac paketleri kendi işletim sistemlerinde derlenmelidir.')
arch='arm64' if platform.machine().lower() in ['arm64','aarch64'] else 'x64'
subprocess.run([sys.executable,str(root/'scripts/runtime_check.py')],check=True)
candidates=[os.environ.get('CONDA_EXE'),shutil.which('conda.exe' if sys.platform=='win32' else 'conda')]
if sys.platform=='win32':candidates.append(str(Path(sys.prefix).parents[1]/'Scripts/conda.exe'))
conda=next((p for p in candidates if p and Path(p).is_file()),None)
if not conda:raise SystemExit('Conda çalıştırıcısı bulunamadı; yerel build ortamını etkinleştirin.')
packages=subprocess.check_output([conda,'list','--json'],text=True)
identifier=hashlib.sha256((packages+(root/'requirements-cad.txt').read_text()).encode()).hexdigest()[:20]
output=root/'build/runtime';output.parent.mkdir(exist_ok=True)
if output.exists():raise SystemExit('build/runtime zaten var. Eski derleme klasörünü kaldırıp yeniden deneyin.')
with tempfile.TemporaryDirectory() as directory:
    archive=Path(directory)/'runtime.tar.gz'
    args=[conda,'run','-n','base','conda-pack','--prefix',sys.prefix,'--output',str(archive)]
    prefix='/Applications/LS MoldWorks.app/Contents/Resources/runtime'
    if sys.platform=='darwin':args+=['--dest-prefix',prefix]
    subprocess.run(args,check=True)
    output.mkdir()
    with tarfile.open(archive) as tar:tar.extractall(output,filter='tar')
if sys.platform=='darwin':subprocess.run([sys.executable,str(root/'scripts/sign-macos-runtime.py'),str(output)],check=True)
manifest={'id':identifier,'platform':sys.platform,'arch':arch,'relocation':'fixed' if sys.platform=='darwin' else 'first-run'}
if sys.platform=='darwin':manifest['prefix']=prefix
(output/'runtime-pack.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print('Bağımsız çalışma ortamı hazır:',output)
