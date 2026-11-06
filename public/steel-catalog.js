(function(root){
'use strict';
const version='analiz-v4-2026-11-05';
const normalize=name=>String(name||'').toLocaleUpperCase('tr-TR').replace(/İ/g,'I').replace(/^1[.,](?=\d{4})/,'').replace(/[^A-Z0-9]/g,'');
const steels=[['2312',2.2],['2344',3.9],['W350',12.2],['W360',15.8],['DIEVAR',9.5],['DIE CAST ONE',7.5],['1730',1.5],['2714',2.7],['2343 ESR',4.8],['CK45',43/36]].map(([name,price])=>({name,price,density:8000}));
const identity=name=>{const n=normalize(name);return n==='DCO'?'DIECASTONE':n;};
function hydrate(settings){const result=structuredClone(settings);if(result.steelCatalogVersion===version)return result;const rows=Array.isArray(result.steels)?result.steels:[];const names=new Set(rows.map(s=>identity(s.name)));for(const s of steels)if(!names.has(identity(s.name))){rows.push({...s});names.add(identity(s.name));}result.steels=rows;result.steelCatalogVersion=version;return result;}
root.SteelCatalog={version,steels,services:{heatTreatment:{label:'Isıl işlem',price:2.4,unit:'EUR/kg'},coating:{label:'Kaplama',price:2.7,unit:'EUR/kg'}},normalize,hydrate};
})(typeof window==='undefined'?globalThis:window);
