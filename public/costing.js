(function(root){
const defaults={name:'HPDC temel profil',profit:20,trimPercent:100/3,machiningRate:'',designRate:'',assemblyRate:''};
function summarize(a){
 if(a.pricing?.method==='analiz-v4')return CostingV4.summarize(a,Materials.calculate);
 const material=Materials.calculate(a.material||{}),lines=[],issues=[];
 if(material.error||material.cost===null||!Number.isFinite(material.cost))issues.push('Çekirdek blok ölçüleri / çelik kg fiyatı tamamlanmadı.');
 const rawCost=material.error||!Number.isFinite(material.cost)?null:material.cost;
 let subtotal=rawCost??0;
 for(const [i,line] of (a.costLines||[]).entries()){
  if(line.included===false||(line.technicalGenerated&&line.category==='core'&&a.core!=='included'))continue;
  const qty=Number(line.quantity),rate=Number(line.rate);
  if(line.quantity===''||line.rate===''||!Number.isFinite(qty)||qty<=0||!Number.isFinite(rate)||rate<0){issues.push(`Maliyet satırı ${i+1}: miktar veya birim fiyat eksik / geçersiz.`);lines.push({...line,total:null});continue;}
  const total=qty*rate;if(!Number.isFinite(total)){issues.push(`Maliyet satırı ${i+1}: hesap sınırı aşıldı.`);lines.push({...line,total:null});continue;}subtotal+=total;lines.push({...line,total});
 }
 const pricing={...defaults,...a.pricing};const profit=Number(pricing.profit);
 if(pricing.profit===''||!Number.isFinite(profit)||profit<0)issues.push('Maliyet üzerine kâr oranı geçersiz.');
 if(!Number.isFinite(subtotal*(1+profit/100)))issues.push('Hesap sınırı aşıldı.');const complete=issues.length===0;
 return {rawCost,material,lines,subtotal,complete,issues,profit:pricing.profit,suggestedCasting:complete?subtotal*(1+profit/100):null};
}
function roundMoney(value){if(value===null||!Number.isFinite(value)||Math.abs(value)>Number.MAX_SAFE_INTEGER/100)return null;return Math.round((value+Number.EPSILON)*100)/100;}
function quote(a){const p={...defaults,...a.pricing},r=summarize(a),auto=p.mode==='calculated';const raw=auto?r.suggestedCasting:(a.cost!==''&&a.cost!=null&&Number.isFinite(Number(a.cost))&&Number(a.cost)>=0?Number(a.cost):null),casting=roundMoney(raw);const ratio=Number(p.trimPercent);const trimValid=p.trimPercent!==''&&Number.isFinite(ratio)&&ratio>=0;const trim=p.trimEnabled?(casting!==null&&trimValid?roundMoney(casting*ratio/100):null):0;const total=casting!==null&&trim!==null?roundMoney(casting+trim):null;return {casting,trim,total,complete:total!==null};}

root.Costing={defaults,summarize,quote};
})(globalThis);
