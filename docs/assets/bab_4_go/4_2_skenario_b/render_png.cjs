// Usage: node render_png.cjs INPUT.svg OUTPUT.png
const sharp=require('/Users/david/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/sharp');
sharp(process.argv[2],{density:300}).png().toFile(process.argv[3]).catch(e=>{process.stderr.write(String(e));process.exit(1)});
