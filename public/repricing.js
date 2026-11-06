(function(root){
const normalize=v=>String(v||'').trim().toLocaleLowerCase('tr');
function create(source,settings,at=new Date().toISOString()){
 const a=structuredClone(source),notes=[];delete a.actualCosts;a.id=crypto.randomUUID();a.offerIncluded=true;a.label='Güncel fiyatlar · '+at.slice(0,10).split('-').reverse().join('.');
 const previous=Costing.quote(source),profile=structuredClone(settings.costProfile||Costing.defaults);a.costProfile={...profile,snapshotAt:at};a.pricing={...a.pricing,...profile,mode:'calculated'};
 const steel=(settings.steels||[]).filter(s=>normalize(s.name)===normalize(source.material?.steelName)&&normalize(s.name));a.material={...a.material};
 if(steel.length===1&&steel[0].price!==''&&steel[0].price!=null){a.material.price=steel[0].price;a.material.priceUpdatedAt=steel[0].updatedAt||'';a.material.priceAtRate=String(steel[0].price);}else{a.material.price='';notes.push('Çekirdek çeliği güncel katalogda tekil ve fiyatlı olarak bulunamadı. Çelik seçin.');}
 a.costLines=(source.costLines||[]).map(line=>{const next=structuredClone(line);if(line.included===false)return next;let price=null,priceDate='';
 if(!line.manualRateOverride&&line.rateSource?.type==='piston'){const matches=(settings.pistons||[]).filter(p=>normalize(p.brand)===normalize(line.rateSource.brand)&&normalize(p.model)===normalize(line.rateSource.model));if(matches.length===1){price=matches[0].price;priceDate=matches[0].updatedAt||'';}}
 else if(!line.manualRateOverride&&line.rateSource?.type==='steel'){const matches=(settings.steels||[]).filter(s=>normalize(s.name)===normalize(line.rateSource.name));if(matches.length===1){price=matches[0].price;priceDate=matches[0].updatedAt||'';}}
 else if(!line.manualRateOverride&&line.rateSource?.type==='v4'&&globalThis.CostingV4?.operations[line.rateSource.key])price=profile.v4Rates?.[line.rateSource.key]??CostingV4.operations[line.rateSource.key].rate;
 else if(!line.manualRateOverride&&line.rateSource?.type==='profile'&&line.rateSource.key===line.category&&['machining','design','assembly'].includes(line.category)){price=profile[{machining:'machiningRate',design:'designRate',assembly:'assemblyRate'}[line.category]];}
 if(price===''||price==null){next.rate='';notes.push((line.description||'Maliyet kalemi')+': güncel birim fiyatı elle tamamlayın.');}else{next.rate=price;if(next.rateSource)next.rateSource.updatedAt=priceDate;}return next;});
 if(a.technical){for(const prefix of ['insert','base','core','fixedInsert','movingInsert','fixedBase','movingBase']){const name=a.technical[prefix+'SteelName'];if(!name)continue;const matches=(settings.steels||[]).filter(s=>normalize(s.name)===normalize(name));a.technical[prefix+'Price']=matches.length===1?matches[0].price:'';a.technical[prefix+'UpdatedAt']=matches.length===1?matches[0].updatedAt||'':'';}}const q=Costing.quote(a);a.cost=q.casting===null?'':String(Math.round(q.casting*100)/100);a.repricedFrom={alternativeId:source.id,at,previousCasting:previous.casting,previousTrim:previous.trim,previousTotal:previous.total,notes};
 return {alternative:a,notes,previous,current:q};
}
root.Repricing={create};
})(globalThis);
