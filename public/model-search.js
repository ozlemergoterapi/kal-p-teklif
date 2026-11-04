(function(root){
function valid(g){return g&&g.version==='solid-invariants-v1'&&g.units==='mm'&&Number.isInteger(g.solids)&&g.solids>0&&[g.volume,g.area].every(v=>Number.isFinite(v)&&v>0)&&Array.isArray(g.inertia)&&g.inertia.length===3&&g.inertia.every(v=>Number.isFinite(v)&&v>0)&&Array.isArray(g.bounds)&&g.bounds.length===3&&g.bounds.every(v=>Number.isFinite(v)&&v>0);}
function compare(a,b){if(!valid(a)||!valid(b)||a.solids!==b.solids)return null;const delta=(x,y)=>Math.abs(x-y)/Math.max(x,y);const volume=delta(a.volume,b.volume),area=delta(a.area,b.area),inertia=Math.max(...[...a.inertia].sort((a,b)=>a-b).map((v,i)=>delta(v,[...b.inertia].sort((a,b)=>a-b)[i])));const maximum=Math.max(volume,area,inertia);if(maximum>.12)return null;return {volume,area,inertia,maximum,level:maximum<=.02?'close':'similar'};}
root.ModelSearch={valid,compare};
})(globalThis);
