import http from 'node:http';
import {readFile,mkdtemp,writeFile,rm} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import {tmpdir} from 'node:os';
import {spawn as spawnChild} from 'node:child_process';
const children=new Set();function spawn(command,args,options={}){const child=spawnChild(command,args,{...options,env:{...process.env,...options.env,PYTHONUTF8:'1',PYTHONIOENCODING:'utf-8'},windowsHide:true});children.add(child);child.once('close',()=>children.delete(child));return child;}
for(const signal of ['SIGTERM','SIGINT'])process.on(signal,()=>{for(const child of children)child.kill();process.exit(0);});
import path from 'node:path';
const root=path.resolve(fileURLToPath(new URL('./public/',import.meta.url)));
const script=fileURLToPath(new URL('./scripts/geometry.py',import.meta.url));
const meshScript=fileURLToPath(new URL('./scripts/mesh.py',import.meta.url));
const types={'.html':'text/html; charset=utf-8','.css':'text/css','.js':'text/javascript','.png':'image/png'};
function worker(script,args,limit=120000){return new Promise((resolve,reject)=>{const child=spawn(process.env.LS_CAD_PYTHON||'python3',[fileURLToPath(new URL('./scripts/'+script,import.meta.url)),...args],{stdio:['ignore','pipe','pipe']});let output='',error='',done=false;const finish=(e)=>{if(done)return;done=true;clearTimeout(timer);e?reject(e):resolve(output);};const timer=setTimeout(()=>{child.kill('SIGKILL');finish(new Error('Analiz süre sınırını aştı.'));},limit);child.stdout.on('data',d=>{output+=d;if(output.length>3*1024*1024){child.kill('SIGKILL');finish(new Error('Belge çıktı sınırı aşıldı.'));}});child.stderr.on('data',d=>error=(error+d).slice(-2000));child.on('error',()=>finish(new Error('Analiz ortamı başlatılamadı.')));child.on('close',code=>finish(code?new Error(error||'Dosya analiz edilemedi.'):null));});}
let documentBusy=false;
async function documentAnalysis(req,res){if(documentBusy){req.resume();json(res,429,{error:'Başka belge inceleniyor.'});return;}if(req.headers.origin&&![`http://${req.headers.host}`,`https://${req.headers.host}`].includes(req.headers.origin)){req.resume();json(res,403,{error:'İstek kaynağı kabul edilmedi.'});return;}let dir;documentBusy=true;try{const ext=path.extname(new URL(req.url,'http://localhost').searchParams.get('filename')||'').toLowerCase();if(!['.pdf','.eml','.msg','.txt','.dxf','.png','.jpg','.jpeg','.webp'].includes(ext))throw new Error('Belge biçimi desteklenmiyor.');let size=0;const chunks=[];for await(const chunk of req){size+=chunk.length;if(size>30*1024*1024)throw new Error('Belge 30 MB sınırını aşıyor.');chunks.push(chunk);}dir=await mkdtemp(path.join(tmpdir(),'ls-document-'));const filename=path.join(dir,'document'+ext);await writeFile(filename,Buffer.concat(chunks));const result=JSON.parse(await worker('documents.py',[filename],180000));if(result.error)throw new Error(result.error);json(res,200,result);}catch(e){json(res,422,{error:e.message});}finally{documentBusy=false;if(dir)await rm(dir,{recursive:true,force:true});}}
let analyzing=false;
function json(res,status,value){res.writeHead(status,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'}).end(JSON.stringify(value));}
async function geometry(req,res,mesh=false){
 if(analyzing){req.resume();json(res,429,{error:'Başka model analiz ediliyor. Biraz sonra dosyayı yeniden seçin.'});return;}
 // This local prototype accepts same-origin browser requests only.
 if(req.headers.origin&&req.headers.origin!==`http://${req.headers.host}`&&req.headers.origin!==`https://${req.headers.host}`){req.resume();json(res,403,{error:'İstek kaynağı kabul edilmedi.'});return;}
 analyzing=true;let dir;
 try{
  let size=0;const chunks=[];
  for await(const chunk of req){size+=chunk.length;if(size>50*1024*1024){json(res,413,{error:'50 MB sınırı aşıldı.'});return;}chunks.push(chunk);}
  const bytes=Buffer.concat(chunks);
  const ext=path.extname(new URL(req.url,'http://localhost').searchParams.get('filename')||'part.step').toLowerCase();
  if(!['.step','.stp','.igs','.iges','.x_t','.x_b','.catpart','.catproduct'].includes(ext))throw new Error('CAD biçimi desteklenmiyor.');
  dir=await mkdtemp(path.join(tmpdir(),'ls-step-'));let filename=path.join(dir,'part'+ext);await writeFile(filename,bytes);
  if(!['.step','.stp'].includes(ext)){const converted=path.join(dir,'converted.step');await worker('cad_convert.py',[filename,converted],90000);filename=converted;}
  else if(!bytes.subarray(0,128).toString().trimStart().startsWith('ISO-10303-21;'))throw new Error('Geçerli STEP başlığı bulunamadı.');
  const result=await new Promise((resolve,reject)=>{
   const child=spawn(process.env.LS_CAD_PYTHON||'python3',[mesh?meshScript:script,filename],{stdio:['ignore','pipe','ignore'],env:{...process.env,XDG_CACHE_HOME:dir}});
   let output='',done=false;const finish=(err,value)=>{if(done)return;done=true;clearTimeout(timer);err?reject(err):resolve(value);};
   const timer=setTimeout(()=>{child.kill('SIGKILL');finish(new Error('Analiz süre sınırını aştı.'));},120000);
   child.stdout.on('data',data=>{output+=data;if(output.length>(mesh?32*1024*1024:65536)){child.kill('SIGKILL');finish(new Error('Analiz çıktısı geçersiz.'));}});
   child.on('error',()=>finish(new Error('CAD Python ortamı başlatılamadı.')));
   child.on('close',code=>{if(code!==0){finish(new Error('STEP katısı analiz edilemedi. CAD bağımlılıklarını ve dosyayı kontrol edin.'));return;}try{finish(null,JSON.parse(output));}catch{finish(new Error('CAD analiz yanıtı okunamadı.'));}});
  });
  json(res,200,result);
 }catch(error){if(!res.writableEnded)json(res,422,{error:error.message});}
 finally{analyzing=false;if(dir)await rm(dir,{recursive:true,force:true});}
}
let pdfBusy=false;
async function moldReport(req,res,kind='mold'){if(pdfBusy){req.resume();json(res,429,{error:'Ölçü PDF hazırlanıyor; biraz sonra tekrar deneyin.'});return;}if(req.headers.origin&&![`http://${req.headers.host}`,`https://${req.headers.host}`].includes(req.headers.origin)){req.resume();json(res,403,{error:'İstek kaynağı kabul edilmedi.'});return;}pdfBusy=true;let dir;try{const chunks=[];let size=0;for await(const c of req){size+=c.length;if(size>8*1024*1024){json(res,413,{error:'Rapor 8 MB sınırını aşıyor.'});return;}chunks.push(c);}const payload=JSON.parse(Buffer.concat(chunks).toString('utf8'));if(payload.format!==(kind==='quotation'?'ls-quotation-v1':'ls-mold-dimensions-v1'))throw new Error('Rapor biçimi geçersiz.');dir=await mkdtemp(path.join(tmpdir(),'ls-report-'));const input=path.join(dir,'input.json'),output=path.join(dir,'summary.pdf');await writeFile(input,JSON.stringify(payload));await new Promise((resolve,reject)=>{const child=spawn(process.env.LS_CAD_PYTHON||'python3',[fileURLToPath(new URL(kind==='quotation'?'./scripts/quotation_report.py':'./scripts/mold_report.py',import.meta.url)),input,output],{stdio:'ignore'});let done=false;const finish=error=>{if(done)return;done=true;clearTimeout(timer);error?reject(error):resolve();};const timer=setTimeout(()=>{child.kill('SIGKILL');finish(new Error('PDF oluşturma süre sınırını aştı.'));},30000);child.on('error',()=>finish(new Error('PDF Python ortamı açılamadı.')));child.on('close',code=>finish(code===0?null:new Error('Ölçü PDF oluşturulamadı. Rapor verilerini ve PDF bağımlılıklarını kontrol edin.')));});const pdf=await readFile(output);res.writeHead(200,{'Content-Type':'application/pdf','Cache-Control':'no-store'}).end(pdf);}catch(error){if(!res.writableEnded)json(res,422,{error:error.message});}finally{pdfBusy=false;if(dir)await rm(dir,{recursive:true,force:true});}}
http.createServer(async(req,res)=>{try{
 const name=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
 if(name==='/api/health'&&req.method==='GET'){json(res,200,{app:'ls-moldworks',instance:process.env.LS_INSTANCE_ID||'local'});return;}
 if(name==='/api/documents'&&req.method==='POST'){await documentAnalysis(req,res);return;}
 if(name==='/api/capabilities'&&req.method==='GET'){json(res,200,{nativeCAD:['step','stp','igs','iges'],licensedTranslator:!!process.env.LS_CAD_CONVERTER_EXECUTABLE,documents:['pdf','eml','msg','txt','dxf','png','jpg','jpeg','webp']});return;}
 if(name==='/api/quotation-pdf'&&req.method==='POST'){await moldReport(req,res,'quotation');return;}
 if(name==='/api/mold-report'&&req.method==='POST'){await moldReport(req,res);return;}
 if(name==='/api/mesh'&&req.method==='POST'){await geometry(req,res,true);return;}
 if(name==='/api/geometry'&&req.method==='POST'){await geometry(req,res);return;}
 if(!['GET','HEAD'].includes(req.method)){json(res,405,{error:'Yöntem desteklenmiyor.'});return;}
 const file=path.resolve(root,'.'+(name==='/'?'/index.html':name));if(!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
 const data=await readFile(file);res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream'}).end(req.method==='HEAD'?undefined:data);
}catch{res.writeHead(404).end('Not found');}}).listen(Number(process.env.PORT||3000),process.env.HOST||'127.0.0.1',()=>console.log('LS MoldWorks ready on port '+(process.env.PORT||3000)));
