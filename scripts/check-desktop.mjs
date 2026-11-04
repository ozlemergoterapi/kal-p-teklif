import {createRequire} from 'node:module';
import {access} from 'node:fs/promises';
const require=createRequire(import.meta.url),{validateConfiguration}=require('app-builder-lib/out/util/config/config.js'),{DebugLogger}=require('builder-util');
await validateConfiguration(require('../desktop/builder.cjs'),new DebugLogger(false));
for(const file of ['desktop/main.cjs','desktop/preload.cjs','desktop/runtime.cjs','desktop/loading.html','desktop/icon.ico','desktop/icon.icns','desktop/icon.png','desktop/installer/macos/postinstall'])await access(file);
console.log('Windows NSIS ve Mac PKG yapılandırması doğrulandı.');
