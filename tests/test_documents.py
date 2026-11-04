import sys,tempfile,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from documents import parse,extract
class DocumentTests(unittest.TestCase):
    def test_lr_multiple_and_negative_scope(self):
        f=parse('Please quote using a 1+1 eye concept. No cores. Without slides. Trim excluded.');self.assertEqual([x['value'] for x in f if x['kind']=='cavities'],[2]);self.assertTrue(any(x['kind']=='arrangement' and x['value']=='right-left' for x in f));self.assertTrue(any(x['kind']=='core' and x['value']=='none' for x in f));self.assertTrue(any(x['kind']=='trim' and x['value'] is False for x in f))
        self.assertEqual([x['value'] for x in parse('2 ve 4 gözlü teklif, 100 x 80 x 40 mm') if x['kind']=='cavities'],[2,4])
    def test_labeled_dimensions_and_requirements(self):
        f=parse('Length: 100 mm Width: 80 mm Height: 40 mm ADC12 200 ton');self.assertTrue(any(x['kind']=='dimensions' and x['value']==[100,80,40] for x in f));self.assertTrue(any(x['kind']=='press' and x['value']==200 for x in f));self.assertTrue(any(x['kind']=='alloy' for x in f))
    def test_eml_and_vector_pdf(self):
        import fitz
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'request.eml';p.write_text('Subject: Quotation\nContent-Type: text/plain; charset=utf-8\n\n2 cavities; 100 x 80 x 40 mm');self.assertTrue(extract(p)['findings'])
            p=Path(d)/'drawing.pdf';doc=fitz.open();page=doc.new_page();page.insert_text((60,60),'PART 100 x 80 x 40 mm / 4 cavities');doc.save(p);self.assertTrue(any(f['kind']=='dimensions' for f in extract(p)['findings']))
    def test_ocr_image(self):
        from PIL import Image,ImageDraw,ImageFont
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'drawing.png';im=Image.new('RGB',(1500,400),'white');draw=ImageDraw.Draw(im);font=ImageFont.truetype(str(Path(__file__).resolve().parents[1]/'assets/fonts/DejaVuSans.ttf'),55);draw.text((40,100),'PART 100 x 80 x 40 mm',font=font,fill='black');im.save(p);self.assertTrue(any(f['kind']=='dimensions' for f in extract(p)['findings']))
