const sharp=require('/Users/david/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
const fs=require('fs');const path=require('path');
(async()=>{const root=__dirname;for(const f of fs.readdirSync(root).filter(x=>x.endsWith('_cetak.svg'))){await sharp(path.join(root,f),{density:300}).resize({width:1654}).png().toFile(path.join(root,f.replace('.svg','.png')));}console.log('Two PNGs rendered at 300dpi.');})();
