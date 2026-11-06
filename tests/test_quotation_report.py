import importlib.util
import tempfile
import unittest
from pathlib import Path
import fitz

spec=importlib.util.spec_from_file_location('quotation_report',Path(__file__).resolve().parents[1]/'scripts/quotation_report.py')
report=importlib.util.module_from_spec(spec);spec.loader.exec_module(report)

class QuotationReportTests(unittest.TestCase):
    def page(self,title='FİYAT TEKLİFİ - KP26001'):
        return dict(title=title,draft='',option='Alternatif 1 · 2 göz',company=dict(name='Örnek Kalıp',address='İstanbul',contact='teklif@example.com',preparedBy='Hazırlayan',logo=''),customer=[['Müşteri','Örnek müşteri']],metadata=[['Teklif No','KP26001'],['Revizyon','1']],general='Genel Bilgiler',headers=['Parametre','Malzeme','Ölçüler','Parça Görünüşü'],rows=[['Çekirdek '+str(i),'W360','100 × 80 × 60'] for i in range(27)],image='',imageMissing='Görsel yok',priceHeaders=['No','Açıklama','Tip','Not','Teslim','Fiyat (€)'],items=[[1,'Gövde','Döküm kalıbı','2 göz','10 hafta','300,00'],[2,'Gövde','Trim kalıbı','','+2 hafta','100,00']],totalLabel='Toplam fiyat (€)',total='400,00',termsTitle='Satış Şartları ve Koşulları',terms=[['Ödeme','%40 sipariş'],['Geçerlilik','30 gün']],analysis={'title':'Parça inceleme','text':'Ölçüler doğrulandı.'})
    def test_unicode_a4_separate_options_complete_rows_and_no_draft_after_approval(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'quote.pdf';report.create({'format':'ls-quotation-v1','language':'tr','pages':[self.page(),self.page()]},file)
            with fitz.open(file) as pdf:
                self.assertEqual(len(pdf),2)
                for page in pdf:
                    text=page.get_text();self.assertIn('Çekirdek 26',text);self.assertIn('Trim kalıbı',text);self.assertIn('400,00',text);self.assertIn('Ölçüler doğrulandı.',text);self.assertNotIn('ONAYLANMAMIŞ',text)
                    self.assertAlmostEqual(page.rect.width,595.2756,places=2)
                    for word in page.get_text('words'):self.assertLessEqual(word[3],page.rect.height)
    def test_english_draft_marker_and_escaped_markup(self):
        page=self.page('PRICE QUOTATION - KP26001');page['draft']='UNAPPROVED DRAFT';page['rows'][0][1]='<b>Not executable & literal</b>'
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'draft.pdf';report.create({'format':'ls-quotation-v1','language':'en','pages':[page]},file)
            with fitz.open(file) as pdf:text=pdf[0].get_text()
            self.assertIn('UNAPPROVED DRAFT',text);self.assertIn('<b>Not executable & literal</b>',' '.join(text.split()))
    def test_external_image_urls_are_rejected(self):
        page=self.page();page['image']='https://example.com/tracker.png'
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):report.create({'format':'ls-quotation-v1','language':'tr','pages':[page]},Path(d)/'bad.pdf')

if __name__=='__main__':unittest.main()
