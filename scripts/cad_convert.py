"""Native IGES conversion and optional licensed translator adapter."""
import sys,os,subprocess
from pathlib import Path
def convert(source,target):
    ext=Path(source).suffix.lower()
    if ext in ['.igs','.iges']:
        from OCP.IGESControl import IGESControl_Reader
        from OCP.IFSelect import IFSelect_RetDone
        from OCP.STEPControl import STEPControl_Writer,STEPControl_AsIs
        reader=IGESControl_Reader()
        if reader.ReadFile(str(source))!=IFSelect_RetDone or not reader.TransferRoots():raise ValueError('IGES okunamadı.')
        writer=STEPControl_Writer();writer.Transfer(reader.OneShape(),STEPControl_AsIs)
        if writer.Write(str(target))!=IFSelect_RetDone:raise ValueError('IGES STEP dönüşümü başarısız.')
    elif ext in ['.x_t','.x_b','.catpart','.catproduct']:
        executable=os.environ.get('LS_CAD_CONVERTER_EXECUTABLE')
        if not executable:raise ValueError('Bu biçim için lisanslı CAD çevirici kurulmalı. LS_CAD_CONVERTER_EXECUTABLE ayarlayın veya STEP/IGES dışa aktarın.')
        subprocess.run([executable,str(source),str(target)],check=True,timeout=80,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:raise ValueError('CAD biçimi desteklenmiyor.')
    if not Path(target).is_file() or Path(target).stat().st_size>50*1024*1024:raise ValueError('Dönüştürülen STEP geçersiz veya çok büyük.')
if __name__=='__main__':
    try:convert(sys.argv[1],sys.argv[2])
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
