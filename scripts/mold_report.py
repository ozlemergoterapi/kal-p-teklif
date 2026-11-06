"""Create a Unicode, dimensioned technical draft PDF from local orthographic renders."""
import base64
import io
import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4,landscape
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether

FONTS=Path(__file__).resolve().parents[1]/'assets/fonts'
def number(v):
    if not isinstance(v,(int,float)) or not math.isfinite(v) or abs(v)>1e12:raise ValueError('Geçersiz sayısal ölçü.')
    return f'{v:,.2f}'.replace(',','_').replace('.',',').replace('_','.')
def image(data):
    if not isinstance(data,str) or len(data)>6000000 or not data.startswith(('data:image/png;base64,','data:image/jpeg;base64,')):raise ValueError('Görünüş resmi geçersiz.')
    raw=base64.b64decode(data.split(',',1)[1],validate=True)
    with PILImage.open(io.BytesIO(raw)) as p:
        if p.width>2200 or p.height>2200 or p.width<10 or p.height<10:raise ValueError('Görünüş boyutu geçersiz.')
        p.verify()
    return io.BytesIO(raw)
def create(payload,outfile):
    if payload.get('format')!='ls-mold-dimensions-v1':raise ValueError('Rapor biçimi geçersiz.')
    blocks=payload.get('blocks',[]);views=payload.get('views',[])
    if not isinstance(blocks,list) or not 1<=len(blocks)<=512 or len(views)!=3:raise ValueError('Rapor kalemleri geçersiz.')
    en=payload.get('language')=='en';tr=lambda a,b:b if en else a
    pdfmetrics.registerFont(TTFont('LS',str(FONTS/'DejaVuSans.ttf')));pdfmetrics.registerFont(TTFont('LSBold',str(FONTS/'DejaVuSans-Bold.ttf')))
    styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='LSBody',fontName='LS',fontSize=8,leading=12,textColor=colors.HexColor('#526978')));styles.add(ParagraphStyle(name='LSTitle',fontName='LSBold',fontSize=18,leading=23,textColor=colors.HexColor('#102940')));styles.add(ParagraphStyle(name='LSCell',fontName='LS',fontSize=7,leading=10))
    paragraph=lambda v,style='LSBody':Paragraph(escape(str(v))[:4000],styles[style])
    doc=SimpleDocTemplate(str(outfile),pagesize=landscape(A4),rightMargin=26,leftMargin=26,topMargin=24,bottomMargin=30,title=tr('Kalıp Ölçü Özeti','Mold Dimension Summary')+' '+str(payload.get('code','')),author=str(payload.get('issuer','LS MoldWorks')))
    flow=[paragraph(payload.get('issuer') or 'LS MoldWorks'),paragraph(tr('Kalıp Ölçü Özeti','Mold Dimension Summary'),'LSTitle'),paragraph(f"{payload.get('code','')} · {payload.get('customer','')} · {payload.get('part','')}"),paragraph(tr('Alternatif','Option')+f" {payload.get('alternative','')} · "+tr('Göz','Cavities')+f": {payload.get('cavities','')} · "+tr('Açılma ekseni','Opening axis')+f": {payload.get('axis','')} · {payload.get('date','')}"),Spacer(1,8)]
    cards=[]
    for view in views:
        pic=Image(image(view.get('image')),width=251,height=158,kind='proportional')
        cards.append([paragraph(view.get('title','')),pic])
    tables=[Table([[c[0]],[c[1]]],colWidths=[255]) for c in cards]
    flow.extend([Table([tables],colWidths=[263,263,263]),Spacer(1,8)])
    envelope=payload.get('envelope');insert=payload.get('insert');base=payload.get('base')
    for size in [envelope,insert,base]:
        if not isinstance(size,list) or len(size)!=3:raise ValueError('Ölçü dizisi geçersiz.')
    dimensions=lambda size:' × '.join(number(v) for v in size)+' mm'
    flow.append(paragraph(tr('Dış zarf','Overall envelope')+': '+dimensions(envelope)+'   |   '+tr('Ortak çekirdek referansı','Shared insert reference')+': '+dimensions(insert)+'   |   '+tr('Ortak hamil referansı','Shared base reference')+': '+dimensions(base)))
    flow.append(Spacer(1,9))
    headers=[tr('Kod','ID'),tr('Blok / taslak ölçüsü','Block / finished size'), 'U (mm)','V (mm)',tr('Açılma (mm)','Opening (mm)'), 'kg',tr('Yön','Direction'),tr('Hareket (mm)','Travel (mm)')]
    rows=[headers]
    for b in blocks:
        size=b.get('size');
        if not isinstance(size,list) or len(size)!=3:raise ValueError('Blok ölçüsü geçersiz.')
        rows.append([paragraph(b.get('tag',''),'LSCell'),paragraph(str(b.get('label',''))+' / '+tr('Taslak: ','Finished: ')+dimensions(b.get('finishedSize',size)),'LSCell'),*[number(v) for v in size],number(b.get('mass',0)),str(b.get('direction','—')),number(b['stroke']) if b.get('stroke') is not None else '—'])
    table=Table(rows,colWidths=[55,180,70,70,90,65,55,100],repeatRows=1,hAlign='LEFT');table.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),'LS'),('FONTSIZE',(0,0),(-1,-1),7),('FONTNAME',(0,0),(-1,0),'LSBold'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7f2f2')),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#d9e3e9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]));flow.append(table)
    flow.extend([Spacer(1,9),paragraph(tr('Hareket kontrolü','Motion check')+': '+str(payload.get('motionSummary',tr('Çalıştırılmadı','Not run')))),paragraph(tr('Bu rapor ekrandaki ham blok taslağıdır. İşlenmiş cepler ve imalat detayları içermez. Görünüşler sayfaya sığdırılmıştır; ölçüler mm cinsindedir, imalat ölçeği değildir. Maça hareket kontrolü yalnız zarf tabanlı ön incelemedir; başlangıç temasları ve hamil/çekirdek cepleri doğrulanmaz.','This report is a raw-stock draft, without machined pockets or manufacturing details. Views are fitted to the page; dimensions are in mm, not a manufacturing scale. Core motion is a bounding-envelope preview; initial contacts and base/insert pockets are not validated.'))])
    def footer(canvas,document):
        canvas.setFont('LS',7);canvas.setFillColor(colors.HexColor('#7e929e'));canvas.drawString(27,17,tr('LS MoldWorks · TEKNİK TASLAK','LS MoldWorks · TECHNICAL DRAFT'));canvas.drawRightString(815,17,tr('Sayfa','Page')+' '+str(document.page))
    doc.build(flow,onFirstPage=footer,onLaterPages=footer)
if __name__=='__main__':
    try:create(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')),sys.argv[2])
    except Exception as error:print(str(error),file=sys.stderr);sys.exit(1)
