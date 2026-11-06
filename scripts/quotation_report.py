"""Render the supplied quotation form layout from the same model as the HTML preview."""
import base64
import io
import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, Spacer, PageBreak, KeepInFrame

ROOT=Path(__file__).resolve().parents[1]
NAVY=colors.HexColor('#202b34'); BLUE=colors.HexColor('#286c9f'); GREEN=colors.HexColor('#e3ecd7'); YELLOW=colors.HexColor('#f7fba5')

def picture(data,width,height):
    if not data:return None
    if not isinstance(data,str) or len(data)>7000000 or not data.startswith(('data:image/png;base64,','data:image/jpeg;base64,','data:image/webp;base64,')):raise ValueError('Geçersiz resim')
    raw=base64.b64decode(data.split(',',1)[1],validate=True)
    with PILImage.open(io.BytesIO(raw)) as img:
        if img.width>4096 or img.height>4096:raise ValueError('Resim çok büyük')
        w,h=img.size; output=io.BytesIO();img.convert('RGB').save(output,format='PNG');output.seek(0)
    scale=min(width/w,height/h);return Image(output,width=w*scale,height=h*scale)

def create(payload,destination):
    if payload.get('format')!='ls-quotation-v1' or payload.get('language') not in ('tr','en'):raise ValueError('Geçersiz teklif')
    pages=payload.get('pages');
    if not isinstance(pages,list) or not 1<=len(pages)<=128:raise ValueError('Geçersiz alternatif sayısı')
    def check(value,depth=0):
        if depth>10:raise ValueError('Veri çok derin')
        if isinstance(value,str):
            if len(value)>7000000:raise ValueError('Metin çok uzun')
        elif isinstance(value,list):
            if len(value)>100:raise ValueError('Çok fazla satır')
            for v in value:check(v,depth+1)
        elif isinstance(value,dict):
            for v in value.values():check(v,depth+1)
        elif value is not None and not isinstance(value,(int,float,bool)):raise ValueError('Geçersiz veri')
    check(payload)
    pdfmetrics.registerFont(TTFont('Quote',str(ROOT/'assets/fonts/DejaVuSans.ttf')))
    pdfmetrics.registerFont(TTFont('QuoteBold',str(ROOT/'assets/fonts/DejaVuSans-Bold.ttf')))
    normal=ParagraphStyle('q',fontName='Quote',fontSize=7,leading=8.5,spaceAfter=0,wordWrap='CJK')
    bold=ParagraphStyle('qb',parent=normal,fontName='QuoteBold')
    white=ParagraphStyle('qw',parent=bold,textColor=colors.white)
    def text(value,style=normal):return Paragraph(escape(str(value or '')).replace('\n','<br/>'),style)
    width=A4[0]-48
    def table(data,widths,commands=(),heights=None):
        obj=Table(data,colWidths=widths,rowHeights=heights,hAlign='LEFT')
        obj.setStyle(TableStyle([('GRID',(0,0),(-1,-1),.5,colors.black),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),3),('RIGHTPADDING',(0,0),(-1,-1),3),('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2)]+list(commands)))
        return obj
    def bar(label):return table([[text(label,white)]],[width],[('BACKGROUND',(0,0),(-1,-1),NAVY)])
    story=[]
    for index,p in enumerate(pages):
        if len(p['rows'])>60 or not p['items'] or len(p['items'])>10:raise ValueError('Geçersiz tablo')
        parts=[bar(p['title'])]
        if p.get('draft'):parts.append(table([[text(p['draft'],bold)]],[width],[('BACKGROUND',(0,0),(-1,-1),YELLOW)]))
        if p.get('option'):parts.append(table([[text(p['option'],bold)]],[width]))
        company=p['company'];logo=picture(company.get('logo'),width*.34,45)
        parts.append(table([['',logo or text(company['name'],bold)]],[width*.64,width*.36],[('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white])],[50]))
        client=table([[text(k+':',bold),text(v)] for k,v in p['customer']],[width*.25,width*.39])
        issuer=[table([[text(company['name'],white)]],[width*.36-6],[('BACKGROUND',(0,0),(-1,-1),BLUE)]),text(company['address']),text(company['contact']),text(('Prepared By: ' if payload['language']=='en' else 'Hazırlayan: ')+company['preparedBy'])]
        parties=table([[client,issuer]],[width*.64,width*.36],[('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)])
        parts.extend([parties,Spacer(1,7),table([[text(k+':',bold),text(v)] for k,v in p['metadata']],[width*.25,width*.75]),bar(p['general'])])
        rows=[[text(h,white) for h in p['headers']]]
        image=picture(p.get('image'),width*.34,220) or text(p['imageMissing'])
        for i,row in enumerate(p['rows']):
            if len(row)!=3:raise ValueError('Teknik satır biçimi geçersiz')
            rows.append([text(x) for x in row]+[image if i==0 else ''])
        general=table(rows,[width*.25,width*.21,width*.18,width*.36],[('BACKGROUND',(0,0),(-1,0),BLUE),('SPAN',(3,1),(3,len(rows)-1)),('ALIGN',(3,1),(3,-1),'CENTER')])
        parts.extend([general,Spacer(1,10)])
        prices=[[text(x,bold) for x in p['priceHeaders']]]+[[text(x) for x in r] for r in p['items']]+[[text(p['totalLabel'],bold),'','','','',text(p['total'],bold)]]
        parts.append(table(prices,[width*n for n in [.05,.31,.17,.17,.14,.16]],[('BACKGROUND',(0,0),(-1,0),GREEN),('BACKGROUND',(0,1),(-1,-2),YELLOW),('BACKGROUND',(0,-1),(-1,-1),GREEN),('SPAN',(0,len(prices)-1),(4,len(prices)-1))]))
        parts.extend([Spacer(1,12),bar(p['termsTitle']),table([[text(k),text(v)] for k,v in p['terms']],[width*.25,width*.75])])
        if p.get('analysis'):
            parts.extend([Spacer(1,7),table([[text(p['analysis']['title'],bold)],[text(p['analysis']['text'])]],[width])])
        story.append(KeepInFrame(width,A4[1]-52,parts,mode='shrink',hAlign='LEFT',vAlign='TOP'))
        if index<len(pages)-1:story.append(PageBreak())
    SimpleDocTemplate(str(destination),pagesize=A4,leftMargin=24,rightMargin=24,topMargin=24,bottomMargin=24,title=pages[0]['title'],author=pages[0]['company']['name']).build(story)

if __name__=='__main__':create(json.loads(Path(sys.argv[1]).read_text()),sys.argv[2])
