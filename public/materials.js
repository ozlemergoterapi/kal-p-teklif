/* Versioned, provisional estimating rules; not manufacturing design approval. */
(function(root){
function calculate(p){
 const number=(key,zero=false)=>{const raw=p[key];if(raw===''||raw==null)return null;const v=Number(raw);return Number.isFinite(v)&&(zero?v>=0:v>0)?v:null;};
 const x=number('partX'),y=number('partY'),size=number('referenceSize'),base=number('edge'),threshold=number('threshold'),growth=number('growth',true),cols=number('columns'),rows=number('rows'),gap=number('gap',true),qty=number('quantity'),density=number('density'),thickness=number('thickness');
 if([x,y,base,threshold,growth,cols,rows,gap,qty,density].some(v=>v===null)||![cols,rows,qty].every(Number.isInteger))return {error:'Parça ölçüleri, yerleşim, adet ve kural değerlerini kontrol edin.'};
 const reference=Math.max(x,y,size||0),margin=base+Math.max(0,reference-threshold)*growth;
 const suggestedX=cols*x+(cols-1)*gap+2*margin,suggestedY=rows*y+(rows-1)*gap+2*margin;
 const length=p.manualX!==''&&p.manualX!=null?number('manualX'):suggestedX,width=p.manualY!==''&&p.manualY!=null?number('manualY'):suggestedY;
 if(length===null||width===null)return {error:'Manuel blok ölçüleri pozitif olmalı.'};
 const mass=thickness===null?null:length*width*thickness*density/1e9*qty,price=number('price',true);
 return {reference,margin,suggestedX,suggestedY,length,width,thickness,mass,cost:mass!==null&&price!==null?mass*price:null,tooSmall:length<suggestedX||width<suggestedY};
}
root.Materials={calculate,version:'edge-rule-v2'};
})(typeof globalThis!=='undefined'?globalThis:this);
