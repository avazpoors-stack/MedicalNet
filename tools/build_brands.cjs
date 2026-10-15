// Injects brand logo symbols (Simple Icons, CC0 path data) into index.html between markers. Idempotent.
const fs = require('fs'), path = require('path');
const si = require('simple-icons');
const file = path.join(__dirname, '../index.html');
const pick = { dropbox: si.siDropbox, notion: si.siNotion, github: si.siGithub, linear: si.siLinear };
let out = Object.entries(pick).map(([k, ic]) => `<symbol id="b-${k}" viewBox="0 0 24 24"><path d="${ic.path}"/></symbol>`).join('\n    ');
out += `\n    <symbol id="b-microsoft" viewBox="0 0 24 24"><rect x="1" y="1" width="10.5" height="10.5" fill="#f25022"/><rect x="12.5" y="1" width="10.5" height="10.5" fill="#7fba00"/><rect x="1" y="12.5" width="10.5" height="10.5" fill="#00a4ef"/><rect x="12.5" y="12.5" width="10.5" height="10.5" fill="#ffb900"/></symbol>`;
out += `\n    <symbol id="b-slack" viewBox="0 0 24 24"><rect x="7.2" y="2" width="3.4" height="20" rx="1.7" fill="#36c5f0"/><rect x="13.4" y="2" width="3.4" height="20" rx="1.7" fill="#2eb67d"/><rect x="2" y="7.2" width="20" height="3.4" rx="1.7" fill="#e01e5a"/><rect x="2" y="13.4" width="20" height="3.4" rx="1.7" fill="#ecb22e"/></symbol>`;
let html = fs.readFileSync(file, 'utf8');
const block = `<!--BRAND_SYMBOLS-->\n    ${out}\n    <!--/BRAND_SYMBOLS-->`;
html = /<!--BRAND_SYMBOLS-->[\s\S]*?<!--\/BRAND_SYMBOLS-->/.test(html) ? html.replace(/<!--BRAND_SYMBOLS-->[\s\S]*?<!--\/BRAND_SYMBOLS-->/, block) : html.replace('<!--BRAND_SYMBOLS-->', block);
fs.writeFileSync(file, html);
console.log('brands ok');
