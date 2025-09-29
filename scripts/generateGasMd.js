const fs = require('fs');
const path = require('path');
const txt = path.join(process.cwd(), 'reports', 'gas-report.txt');
const json = path.join(process.cwd(), 'reports', 'gas-report.json');
const ts = new Date().toISOString().replace(/[:.]/g,'-');
const out = path.join(process.cwd(), 'reports', `gas-report-${ts}.md`);
let lines = [`# Gas report ${ts}`, ''];

if (fs.existsSync(txt)) lines.push('## Raw text', '```', fs.readFileSync(txt,'utf8'), '```');
if (fs.existsSync(json)) {
  try { lines.push('## JSON', '```json', fs.readFileSync(json,'utf8'), '```'); } catch(e){}
}
fs.writeFileSync(out, lines.join('\n'));
console.log('Wrote', out);
