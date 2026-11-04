(function(root){
function vector(axis,direction){const world='XYZ'.indexOf(direction?.[0]),local=(MoldPlan.axes[axis]||[]).indexOf(world);if(local<0||!['+','-'].includes(direction?.[1]))return null;const v=[0,0,0];v[local]=direction[1]==='-'?-1:1;return v;}
function bounds(center,size){return {min:center.map((v,i)=>v-size[i]/2),max:center.map((v,i)=>v+size[i]/2)};}
function overlap(a,b){return [0,1,2].reduce((v,i)=>v*Math.max(0,Math.min(a.max[i],b.max[i])-Math.max(a.min[i],b.min[i])),1);}
function coreIndex(block){return Number(block.id.match(/^core(\d+)/)?.[1]||0);}
function position(block,state,t){const core=state.cores[coreIndex(block)],v=vector(state.axis,core.direction);if(!v)return [...block.center];return block.center.map((p,i)=>p+v[i]*Number(core.stroke||0)*Math.max(0,Math.min(1,t)));}
function suggestStroke(mesh,state,core){const v=vector(state.axis,core.direction);if(!v)return 0;const local=v.findIndex(n=>n!==0),size=MoldPlan.dimensions(mesh)[MoldPlan.axes[state.axis][local]],center=[core.x,core.y,core.z][local],width=[core.u,core.v,core.w][local];return Math.ceil(Math.max(0,v[local]>0?size/2-(center-width/2):size/2+center+width/2)+5);}
function prepare(mesh,state,plan){const moving=plan.blocks.filter(b=>b.kind==='core');if(moving.length>64)throw new Error('Hareket ön izlemesi en fazla 64 maça bloğu destekler.');if(!moving.length)throw new Error('Önce en az bir etkin maça bloğu ekleyin.');for(const b of moving){const c=state.cores[coreIndex(b)];if(!vector(state.axis,c.direction))throw new Error('Her etkin maça için çıkarma yönünü seçin.');if(!Number.isFinite(Number(c.stroke))||Number(c.stroke)<0||Number(c.stroke)>1000000)throw new Error('Maça hareket mesafesi geçersiz.');}
const partSize=plan.map.map(i=>plan.part[i]),parts=plan.instances.map((i,index)=>({id:'G'+(index+1),box:bounds(i.center,partSize)})),pairs=[];
for(let i=0;i<moving.length;i++){const a=moving[i];for(const part of parts)pairs.push({a,b:part.id,part:part.box,baseline:overlap(bounds(a.center,a.size),part.box)});for(let j=i+1;j<moving.length;j++){const b=moving[j];pairs.push({a,b,baseline:overlap(bounds(a.center,a.size),bounds(b.center,b.size))});}}
return {moving,pairs,state};}
function at(prepared,t){const boxes=new Map(prepared.moving.map(b=>[b.id,bounds(position(b,prepared.state,t),b.size)])),collisions=[];for(const pair of prepared.pairs){const a=boxes.get(pair.a.id),b=pair.part||boxes.get(pair.b.id),volume=overlap(a,b),threshold=Math.max(.001,pair.baseline*1e-6);if(volume>pair.baseline+threshold)collisions.push({a:pair.a.id,b:pair.part?pair.b:pair.b.id,progress:t,additionalVolume:volume-pair.baseline});}return collisions;}
function scan(prepared,steps=40){const found=new Map();for(let i=1;i<=steps;i++)for(const hit of at(prepared,i/steps)){const key=hit.a+'|'+hit.b;if(!found.has(key))found.set(key,hit);}return [...found.values()];}
root.CoreMotion={vector,bounds,overlap,coreIndex,position,suggestStroke,prepare,at,scan};
})(globalThis);
