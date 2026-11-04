import {mkdir,copyFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=new URL('../',import.meta.url),target=new URL('public/vendor/',root);
await mkdir(target,{recursive:true});
for(const [source,dest] of [['build/three.module.js','three.module.js'],['build/three.core.js','three.core.js'],['examples/jsm/controls/OrbitControls.js','OrbitControls.js'],['LICENSE','THREE-LICENSE.txt']])await copyFile(fileURLToPath(new URL('node_modules/three/'+source,root)),fileURLToPath(new URL(dest,target)));
