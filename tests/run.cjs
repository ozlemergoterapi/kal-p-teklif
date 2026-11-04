// Run in one Node process: this also works where test-runner child IPC is restricted.
const fs=require('node:fs'),path=require('node:path');
for(const name of fs.readdirSync(__dirname).filter(n=>n.endsWith('.cjs')&&n!=='run.cjs').sort())require(path.join(__dirname,name));
