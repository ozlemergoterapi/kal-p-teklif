(function(root){
'use strict';
let provider=()=>[],enabled=()=>true;
const valid3=a=>Array.isArray(a)&&a.length===3&&a.every(n=>Number.isFinite(n)&&n>0&&n<=1000000);
const materialSignature=m=>JSON.stringify(['partX','partY','manualX','manualY','thickness','quantity','columns','rows','gap'].map(k=>m?.[k]??null));
const median=a=>{a.sort((x,y)=>x-y);const i=Math.floor(a.length/2);return a.length%2?a[i]:(a[i-1]+a[i])/2;};
function configure(getProjects,isEnabled=()=>true){provider=getProjects;enabled=isEnabled;}
function samples(){const unique=new Map();for(const p of provider()){if(!root.Workflow.approved(p))continue;for(const a of p.alternatives||[]){if(a.offerIncluded===false)continue;const s=a.technical?.learningSample;if(s?.version!==1||s.cavities!==a.cavities||s.hasCores!==(a.core==='included')||(s.materialSignature&&s.materialSignature!==materialSignature(a.material))||!valid3(s.part)||!valid3(s.fixedInsert)||!valid3(s.movingInsert)||!valid3(s.fixedBase)||!valid3(s.movingBase)||!Number.isInteger(s.cavities)||s.cavities<1||!s.modelHash||![s.edge,s.back,s.wall,s.floor].every(n=>Number.isFinite(n)&&n>=0))continue;const scope=s.workType||a.workType||'new-mold',key=[s.modelHash,scope,s.cavities,s.arrangement,s.axis,s.hasCores].join('|'),item={...s,workType:scope,projectCode:p.code,approvedAt:p.approval.at};if(!unique.has(key)||String(item.approvedAt)>String(unique.get(key).approvedAt))unique.set(key,item);}}return [...unique.values()];}
function recommend(part,state,cavities){if(!enabled()||!valid3(part))return null;const candidates=samples().filter(s=>s.workType===(state.workType||'new-mold')&&s.cavities===cavities&&s.axis===state.axis&&s.arrangement===state.arrangement&&s.hasCores===!!state.expectedCores).map(s=>({...s,distance:part.reduce((d,n,i)=>d+Math.abs(Math.log(n/s.part[i])),0)})).filter(s=>s.part.every((n,i)=>part[i]/n>=.8&&part[i]/n<=1.25)).sort((a,b)=>a.distance-b.distance).slice(0,5);if(!candidates.length)return null;
const m=key=>median(candidates.map(s=>s[key]));const depth=key=>part[2]/2+Math.max(0,median(candidates.map(s=>s[key][2]-s.part[2]/2)));
return {version:1,count:candidates.length,sources:candidates.map(s=>s.projectCode),confidence:candidates.length<3?'limited':'reference',edge:m('edge'),back:m('back'),wall:m('wall'),floor:m('floor'),fixedInsertDepth:depth('fixedInsert'),movingInsertDepth:depth('movingInsert'),fixedBaseDepth:depth('fixedBase'),movingBaseDepth:depth('movingBase'),coreCounts:candidates.map(s=>s.coreCount)};
}
root.PersonalSizing={configure,samples,recommend,materialSignature};
})(typeof window==='undefined'?globalThis:window);
