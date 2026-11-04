"""Installer/runtime preflight; no network and no dependency installation at runtime."""
import importlib,subprocess,shutil,os
for module in ['OCP','numpy','reportlab','PIL','fitz','ezdxf']:importlib.import_module(module)
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
assert not BRepPrimAPI_MakeBox(1,2,3).Shape().IsNull()
ocr=shutil.which('tesseract')
if not ocr:raise RuntimeError('Paketlenmiş OCR bileşeni bulunamadı.')
result=subprocess.run([ocr,'--list-langs'],capture_output=True,text=True,check=True,timeout=20)
if 'eng' not in result.stdout.split():raise RuntimeError('OCR eng dil verisi pakette bulunamadı.')
print('CAD, PDF ve OCR hazır.')
