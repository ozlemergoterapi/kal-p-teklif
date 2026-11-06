(function(root){
'use strict';
// Dimension-only reference profiles. These are stock groups, not finished plate drawings.
const profiles=[
{id:'R01',insert:[400,700,400],base:[400,800,660]},
{id:'R02',insert:[600,780,220],base:[790,980,480]},
{id:'R03',insert:[520,780,220],base:[730,980,460]},
{id:'R04',insert:[800,500,250],base:[1000,700,550]}
];
const coreProfiles=[[300,160,95],[180,220,190],[170,260,150],[170,190,190],[50,50,200]];
function suggest(u,v){if(![u,v].every(n=>Number.isFinite(n)&&n>0))return null;let best=null;
for(const p of profiles)for(const swap of [false,true]){const x=p.insert[swap?1:0],y=p.insert[swap?0:1],ratioU=u/x,ratioV=v/y;if(Math.min(ratioU,ratioV)<.5||Math.max(ratioU,ratioV)>2)continue;const score=Math.abs(Math.log(ratioU))+Math.abs(Math.log(ratioV));if(best&&best.score<=score)continue;const scale=Math.sqrt(ratioU*ratioV);best={id:p.id,score,scale,referenceInsert:p.insert.slice(),referenceBase:p.base.slice(),wallU:(p.base[swap?1:0]-x)/2*scale,wallV:(p.base[swap?0:1]-y)/2*scale,insertDepth:p.insert[2]/2*scale,baseDepth:p.base[2]/2*scale,thicknessAssumption:'group-total-split-equally',reviewRequired:true};}
return best;
}
// Core candidates already include geometric clearance. A sample may enlarge a block,
// never shrink it; direction and required core count still come from geometric review.
function suggestCore(size){if(!Array.isArray(size)||size.length!==3||!size.every(n=>Number.isFinite(n)&&n>0))return null;const sorted=size.map((value,index)=>({value,index})).sort((a,b)=>a.value-b.value);let best=null;
for(const [index,raw] of coreProfiles.entries()){const sample=[...raw].sort((a,b)=>a-b),ratios=sorted.map((s,i)=>s.value/sample[i]);if(Math.min(...ratios)<.5||Math.max(...ratios)>2)continue;const score=ratios.reduce((n,r)=>n+Math.abs(Math.log(r)),0);if(best&&best.score<=score)continue;const dimensions=size.slice();sorted.forEach((s,i)=>dimensions[s.index]=Math.max(s.value,sample[i]));best={id:'M'+String(index+1).padStart(2,'0'),score,size:dimensions,reviewRequired:true};}
return best;
}
root.SizingReferences={version:'archive-dimensions-v1',profiles,coreProfiles,suggest,suggestCore};
})(typeof window==='undefined'?globalThis:window);
