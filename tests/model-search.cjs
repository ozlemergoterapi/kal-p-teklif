const {test}=require('node:test'),assert=require('node:assert/strict');require('../public/model-search.js');
const a={version:'solid-invariants-v1',units:'mm',solids:1,volume:100,area:200,inertia:[300,400,500],bounds:[1,2,3]};
test('invariants ignore names, orientation bounds, translation and moment order',()=>{const b={...a,name:'different',bounds:[3,1,2],inertia:[500,300,400]};assert.equal(ModelSearch.compare(a,b).maximum,0);});
test('rejects nonmatching volumes, inertia, solid counts and malformed geometry',()=>{assert.equal(ModelSearch.compare(a,{...a,volume:200}),null);assert.equal(ModelSearch.compare(a,{...a,inertia:[300,400,1000]}),null);assert.equal(ModelSearch.compare(a,{...a,solids:2}),null);assert.equal(ModelSearch.compare(a,{}),null);});
