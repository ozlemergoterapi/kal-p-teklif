"""Local document extraction. Text is data, never executable instructions."""
import sys,json,re,subprocess,tempfile,io
from pathlib import Path
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
class PlainHTML(HTMLParser):
    def __init__(self):super().__init__();self.parts=[]
    def handle_data(self,data):self.parts.append(data)
def ocr(image):
    from PIL import Image,ImageOps
    p=Image.open(io.BytesIO(image));p.thumbnail((3000,3000));p=ImageOps.grayscale(p)
    with tempfile.TemporaryDirectory() as d:
        f=Path(d)/'page.png';p.save(f)
        return subprocess.run(['tesseract',str(f),'stdout','-l','eng','--psm','3'],capture_output=True,text=True,timeout=35,check=True).stdout

def parse(text):
    normalized=text.lower().translate(str.maketrans('çğıöşü','cgiosu'))
    findings=[];pair_spans=[]
    def add(kind,value,evidence):
        if not any(f['kind']==kind and f['value']==value for f in findings):findings.append(dict(kind=kind,value=value,evidence=evidence.strip()[:250]))
    for m in re.finditer(r'(?<!\d)(\d{1,2})\s*\+\s*(\d{1,2})\s*(?:eye|eyes|cavit\w*|goz|sag|sol|right|left|concept)',normalized):
        if m[1]=='1' and m[2]=='1':pair_spans.append(m.span());add('cavities',2,m[0]);add('arrangement','right-left',m[0])
    for m in re.finditer(r'(?<!\d)(\d{1,2})(?:\s*(?:ve|and|/|or|veya)\s*(\d{1,2}))?\s*(?:goz(?:lu)?|cavit(?:y|ies)|eye(?:s)?)',normalized):
        if any(m.start()<end and m.end()>start for start,end in pair_spans):continue
        for value in [m[1],m[2]]:
            if value and 1<=int(value)<=128:add('cavities',int(value),m[0])
    for m in re.finditer(r'(?<![\d.,])(\d+(?:[.,]\d+)?)\s*[x×*]\s*(\d+(?:[.,]\d+)?)\s*[x×*]\s*(\d+(?:[.,]\d+)?)\s*mm\b',normalized):
        values=[float(m[i].replace(',','.')) for i in [1,2,3]]
        if all(0<v<=100000 for v in values):add('dimensions',values,m[0])
    for m in re.finditer(r'\b(?:length|uzunluk|en|x)\s*[:=]\s*(\d+(?:[.,]\d+)?)\s*mm?\b',normalized):
        rest=normalized
        w=re.search(r'\b(?:width|genislik|boy|y)\s*[:=]\s*(\d+(?:[.,]\d+)?)\s*mm?\b',rest)
        h=re.search(r'\b(?:height|yukseklik|thickness|kalinlik|z)\s*[:=]\s*(\d+(?:[.,]\d+)?)\s*mm?\b',rest)
        if w and h:add('dimensions',[float(x.replace(',','.')) for x in [m[1],w[1],h[1]]],m[0]+'; '+w[0]+'; '+h[0])
    for m in re.finditer(r'\b(?:adc\s*12|alsi\d+(?:cu\d+)?|en\s*ac[- ]?\d{4,5}|a380)\b',normalized):add('alloy',m[0].upper(),m[0])
    for m in re.finditer(r'(?<!\d)(\d{2,4})\s*(?:ton|tonne|tons|tonnes)\b',normalized):add('press',int(m[1]),m[0])
    for line in normalized.splitlines():
        if re.search(r'\b(?:no|without)\s+(?:side\s+)?cores?\b|macasiz|maca\s+(?:yok|olmayacak|istenmiyor)',line):add('core','none',line)
        if re.search(r'\b(?:no|without)\s+slides?\b|kizaksiz|kizak\s+(?:yok|olmayacak|istenmiyor)',line):add('slide','none',line)
        if re.search(r'\btrim\b|capak\s*(?:alma|kesme)',line):
            negative=bool(re.search(r'\b(?:no|without)\s+trim|trim\s+(?:yok|haric|olmayacak|excluded|(?:is\s+)?not\s+(?:required|included|requested))',line));add('trim',not negative,line)
    return findings

def extract(filename):
    p=Path(filename);suffix=p.suffix.lower();pages=[];notes=[]
    if suffix=='.pdf':
        import fitz
        with fitz.open(p) as doc:
            if len(doc)>12:notes.append('İlk 12 sayfa incelendi; kalan sayfalar analiz edilmedi.')
            for i,page in enumerate(doc):
                if i>=12:break
                text=page.get_text();method='pdf-text'
                if len(text.strip())<25:text=ocr(page.get_pixmap(matrix=fitz.Matrix(2,2)).tobytes('png'));method='ocr'
                pages.append(dict(page=i+1,text=text[:60000],method=method))
    elif suffix in ['.png','.jpg','.jpeg','.webp']:
        pages=[dict(page=1,text=ocr(p.read_bytes())[:60000],method='ocr')]
    elif suffix=='.eml':
        msg=BytesParser(policy=policy.default).parsebytes(p.read_bytes());body=msg.get_body(preferencelist=('plain','html'))
        text=body.get_content() if body else ''
        if body and body.get_content_type()=='text/html':h=PlainHTML();h.feed(text);text='\n'.join(h.parts)
        pages=[dict(page=1,text='Subject: '+str(msg.get('Subject',''))+'\n'+text,method='email')]
    elif suffix=='.msg':
        import extract_msg
        msg=extract_msg.Message(str(p))
        try:
            body=msg.body or ''
            if not body and msg.htmlBody:
                raw=msg.htmlBody
                h=PlainHTML();h.feed(raw.decode('utf-8',errors='replace') if isinstance(raw,bytes) else raw);body='\n'.join(h.parts)
            pages=[dict(page=1,text=('Subject: '+str(msg.subject or '')+'\n'+body)[:200000],method='outlook-msg')]
            if msg.attachments:notes.append('Outlook e-postası metni incelendi. Eklerdeki model ve çizimleri ayrıca proje dosyası olarak yükleyin.')
        finally:msg.close()
    elif suffix=='.txt':pages=[dict(page=1,text=p.read_text(encoding='utf-8-sig',errors='replace')[:200000],method='text')]
    elif suffix=='.dxf':
        import ezdxf
        doc=ezdxf.readfile(p);lines=[]
        for e in doc.modelspace():
            if e.dxftype() in ['TEXT','MTEXT']:lines.append(e.dxf.text if e.dxftype()=='TEXT' else e.plain_text())
            elif e.dxftype()=='DIMENSION':lines.append('Ölçü: '+str(e.get_measurement()))
        pages=[dict(page=1,text='\n'.join(lines)[:200000],method='dxf-text')];notes.append('DXF ölçüleri görünüş/ölçek ve birim kontrolü gerektirir; çizim sınırları parça ölçüsü sayılmaz.')
    else:raise ValueError('Belge biçimi desteklenmiyor. PDF, EML, MSG, TXT, DXF veya görüntü kullanın.')
    findings=[]
    for page in pages:
        for f in parse(page['text']):findings.append({**f,'page':page['page'],'method':page['method']})
    return dict(version='document-analysis-v1',pages=pages,findings=findings,notes=notes+['OCR ve ölçü adaylarını belgeyle karşılaştırıp onaylayın. 2D görünüşlerden maça ihtiyacı otomatik doğrulanmaz.'])
if __name__=='__main__':
    try:print(json.dumps(extract(sys.argv[1]),ensure_ascii=False))
    except Exception as e:print(json.dumps({'error':str(e)}));sys.exit(1)
