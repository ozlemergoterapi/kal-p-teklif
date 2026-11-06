// Install the actual PKG and exercise the shipped runtime and desktop service,
// with no Conda/Homebrew paths inherited from the CI build environment.
import {readdir,readFile} from 'node:fs/promises';
import {spawn,spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
import path from 'node:path';
if(process.platform!=='darwin')throw Error('Native macOS test required');
const packages=(await readdir('dist')).filter(f=>f.endsWith('.pkg'));
if(packages.length!==1)throw Error('Expected exactly one PKG');
const installed=spawnSync('/usr/bin/sudo',['/usr/sbin/installer','-pkg',path.resolve('dist',packages[0]),'-target','/'],{stdio:'inherit'});
if(installed.status!==0)throw Error('PKG installation failed');
const app='/Applications/LS MoldWorks.app',resources=path.join(app,'Contents/Resources'),appRoot=path.join(resources,'app');
const require=createRequire(import.meta.url),{prepareRuntime}=require(path.join(appRoot,'desktop/runtime.cjs'));
const env={...process.env,PATH:'/usr/bin:/bin:/usr/sbin:/sbin'};
for(const key of Object.keys(env))if(/^(CONDA|PYTHON|LS_CAD_PYTHON|TESSDATA_PREFIX)/.test(key))delete env[key];
const oldEnv=process.env;process.env=env;
try{await prepareRuntime({resources,userData:path.join(process.env.RUNNER_TEMP,'ls-installed-runtime-test'),appRoot,status:console.log});}finally{process.env=oldEnv;}
console.log('Installed PKG runtime passed CAD, PDF and OCR preflight without build tools.');
const child=spawn(path.join(app,'Contents/MacOS/LS MoldWorks'),[],{env,stdio:['ignore','pipe','pipe']});let diagnostic='',closed=false;
child.stdout.on('data',d=>diagnostic=(diagnostic+d).slice(-6000));child.stderr.on('data',d=>diagnostic=(diagnostic+d).slice(-6000));child.on('exit',()=>closed=true);
try{
 let ready=false;
 for(let i=0;i<120;i++){
  if(closed)throw Error('Installed desktop app exited early. '+diagnostic);
  try{const r=await fetch('http://127.0.0.1:47851/api/health',{signal:AbortSignal.timeout(500)});const health=await r.json();if(r.ok&&health.instance){const page=await fetch('http://127.0.0.1:47851/');if(!page.ok||!(await page.text()).includes('LS MoldWorks'))throw Error('Desktop page missing');ready=true;break;}}catch{}
  await new Promise(r=>setTimeout(r,500));
 }
 if(!ready)throw Error('Installed desktop app did not become ready. '+diagnostic);
 const manifest=JSON.parse(await readFile(path.join(resources,'runtime/runtime-pack.json'),'utf8'));
 console.log('Installed desktop app opened successfully: '+manifest.platform+' '+manifest.arch);
}finally{child.kill('SIGTERM');}
