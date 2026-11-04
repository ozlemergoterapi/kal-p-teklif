import {readdirSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
const root=fileURLToPath(new URL('../',import.meta.url));
const files=['server.mjs',...readdirSync(path.join(root,'desktop')).filter(f=>/\.(cjs|js)$/.test(f)).map(f=>'desktop/'+f),...readdirSync(path.join(root,'public')).filter(f=>f.endsWith('.js')).map(f=>'public/'+f),...readdirSync(path.join(root,'scripts')).filter(f=>f.endsWith('.mjs')).map(f=>'scripts/'+f)];
for(const file of files){const result=spawnSync(process.execPath,['--check',path.join(root,file)],{stdio:'inherit'});if(result.status!==0){process.exitCode=result.status||1;break;}}
if(!process.exitCode)console.log('Syntax checked '+files.length+' JavaScript files.');
