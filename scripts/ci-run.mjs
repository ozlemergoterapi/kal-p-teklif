// Run trusted workflow commands and expose useful errors in GitHub check annotations.
import {spawn} from 'node:child_process';
const [command,...args]=process.argv.slice(2);if(!command)throw Error('CI command required');let tail='';
const child=spawn(command,args,{stdio:['inherit','pipe','pipe'],shell:process.platform==='win32'&&command==='npm'});
const remember=bytes=>{tail=(tail+bytes.toString()).slice(-18000);};child.stdout.on('data',bytes=>{process.stdout.write(bytes);remember(bytes);});child.stderr.on('data',bytes=>{process.stderr.write(bytes);remember(bytes);});
function annotation(message){if(process.env.GITHUB_ACTIONS){const escaped=message.replace(/%/g,'%25').replace(/\r/g,'%0D').replace(/\n/g,'%0A');process.stdout.write('::error title=LS MoldWorks build check::'+escaped+'\n');}}
child.on('error',error=>{annotation(error.message);process.exitCode=1;});child.on('close',code=>{if(code!==0){annotation(tail||'Command failed: '+command);process.exitCode=code||1;}});
