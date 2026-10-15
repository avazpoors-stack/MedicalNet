// Renders proof/health-report.html → proof/health-report.pdf (A4) and a preview screenshot
'use strict';
const path = require('path'); const { chromium } = require('playwright');
const P = path.resolve(__dirname, '..', 'proof');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROME_PATH || '/usr/bin/chromium', args: ['--no-sandbox'] });
  const page = await b.newPage({ viewport: { width: 1280, height: 900 } });
  await page.goto('file://' + path.join(P, 'health-report.html'), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: '/home/user/template_check/shots/report_top.jpg', quality: 70, type: 'jpeg' });
  await page.evaluate(() => document.querySelectorAll('section.blk')[3].scrollIntoView());
  await page.screenshot({ path: '/home/user/template_check/shots/report_mid.jpg', quality: 70, type: 'jpeg' });
  await page.emulateMedia({ media: 'print' });
  await page.pdf({ path: path.join(P, 'health-report.pdf'), format: 'A4', printBackground: true, margin: { top: '10mm', bottom: '10mm', left: '8mm', right: '8mm' } });
  console.log('pdf ok, fonts:', await page.evaluate(() => [...document.fonts].map((f) => f.family + ':' + f.status).join(' ')));
  await b.close();
})();
