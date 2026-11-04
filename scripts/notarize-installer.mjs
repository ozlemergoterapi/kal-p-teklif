import {readdir} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
const keys=['APPLE_ID','APPLE_APP_SPECIFIC_PASSWORD','APPLE_TEAM_ID'],present=keys.map(k=>!!process.env[k]);
if(process.platform!=='darwin'||present.every(v=>!v)){console.log('Mac paket notarization: bu derlemede etkin değil.');process.exit(0);}
if(!present.every(Boolean))throw new Error('Mac doğrulama hesap alanları eksik; dağıtım paketi tamamlanmadı.');
const packages=(await readdir('dist')).filter(n=>n.endsWith('.pkg'));
if(!packages.length)throw new Error('Doğrulanacak Mac kurulum paketi bulunamadı.');
function run(args){const r=spawnSync('xcrun',args,{stdio:'inherit'});if(r.error||r.status!==0)throw new Error('Mac kurulum paketi doğrulanamadı.');}
for(const name of packages){const file='dist/'+name;run(['notarytool','submit',file,'--apple-id',process.env.APPLE_ID,'--password',process.env.APPLE_APP_SPECIFIC_PASSWORD,'--team-id',process.env.APPLE_TEAM_ID,'--wait']);run(['stapler','staple',file]);run(['stapler','validate',file]);}
