const {contextBridge,ipcRenderer}=require('electron');
contextBridge.exposeInMainWorld('startup',{onStatus(callback){ipcRenderer.on('startup-status',(_event,message)=>{if(typeof message==='string')callback(message);});}});
