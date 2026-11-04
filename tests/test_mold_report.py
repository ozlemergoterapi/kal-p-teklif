import base64,io,sys,tempfile,unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from mold_report import create
class ReportTest(unittest.TestCase):
    def payload(self):
        stream=io.BytesIO();Image.new('RGB',(100,60),'white').save(stream,'PNG')
        view={'title':'Üst · Çekirdek','image':'data:image/png;base64,'+base64.b64encode(stream.getvalue()).decode()}
        return dict(format='ls-mold-dimensions-v1',language='tr',code='KP26001',views=[view]*3,blocks=[dict(tag='Ç1',label='Çekirdek',size=[100,80,40],mass=2.512)],envelope=[160,140,160],insert=[100,80,40],base=[160,140,80])
    def test_unicode_reports_and_invalid_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            p=self.payload()
            for lang in ['tr','en']:
                p['language']=lang;out=Path(directory)/(lang+'.pdf');create(p,out);self.assertTrue(out.read_bytes().startswith(b'%PDF-'));self.assertGreater(out.stat().st_size,10000)
            p['blocks'][0]['size'][0]=float('nan')
            with self.assertRaises(ValueError):create(p,Path(directory)/'invalid.pdf')
