(function(root){
let db;const hashPattern=/^[a-f0-9]{64}$/;
async function database(){if(db)return db;db=await new Promise((resolve,reject)=>{const r=indexedDB.open('ls-moldworks-files',2);r.onupgradeneeded=()=>{for(const store of ['files','outputs','meshes'])if(!r.result.objectStoreNames.contains(store))r.result.createObjectStore(store);};r.onsuccess=()=>resolve(r.result);r.onerror=()=>reject(r.error);r.onblocked=()=>reject(new Error('Dosya deposunu güncellemek için uygulamanın eski sekmelerini kapatın.'));});db.onversionchange=()=>{db.close();db=null;};return db;}
async function access(store,mode,fn){const d=await database();return new Promise((resolve,reject)=>{const tx=d.transaction(store,mode);let result;const request=fn(tx.objectStore(store));if(request)request.onsuccess=()=>result=request.result;tx.oncomplete=()=>resolve(result);tx.onerror=()=>reject(tx.error);tx.onabort=()=>reject(tx.error||new Error('Dosya işlemi iptal edildi.'));});}
async function hash(blob){return [...new Uint8Array(await crypto.subtle.digest('SHA-256',await blob.arrayBuffer()))].map(n=>n.toString(16).padStart(2,'0')).join('');}
async function put(expected,blob){if(!hashPattern.test(expected)||!(blob instanceof Blob)||await hash(blob)!==expected)throw new Error('Dosya içerik doğrulaması başarısız.');await access('files','readwrite',s=>s.put(blob,expected));}
async function get(key){if(!hashPattern.test(key||''))return null;return await access('files','readonly',s=>s.get(key))||null;}
function storedName(f){if(!hashPattern.test(f.hash||''))throw new Error('Dosya parmak izi eksik.');const name=(f.name||'dosya').normalize('NFC').replace(/[<>:"/\\|?*\u0000-\u001f]/g,'_').replace(/[. ]+$/g,'').slice(0,100)||'dosya';return f.hash+'--'+name;}
async function outputPut(project,html){await access('outputs','readwrite',s=>s.put({fingerprint:Workflow.content(project),approved:Workflow.approved(project),html},project.id));}
async function outputGet(project){const r=await access('outputs','readonly',s=>s.get(project.id));return r&&r.fingerprint===Workflow.content(project)?r:null;}
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
async function meshGet(hash){return await access('meshes','readonly',s=>s.get(hash))||null;}
async function meshPut(hash,mesh){await access('meshes','readwrite',s=>s.put(mesh,hash));}
root.Attachments={meshGet,meshPut,put,get,hash,storedName,outputPut,outputGet,download};
})(globalThis);
