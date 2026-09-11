// Run after `quarto render`, with _site served on http://localhost:9000.
// Install separately from the legacy Jupyter tests: cd tests/static && npm ci.
const assert = require('node:assert/strict');
const puppeteer = require('puppeteer');
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.EXAMPLES_URL || 'http://localhost:9000/src/examples';
const run = '.exercise-editor-btn-run-code';

async function editCell(page, index, code) {
  await (await page.$$('.cm-content'))[index].click();
  await page.keyboard.down(process.platform === 'darwin' ? 'Meta' : 'Control');
  await page.keyboard.press('KeyA');
  await page.keyboard.up(process.platform === 'darwin' ? 'Meta' : 'Control');
  // Insert as a paste so CodeMirror does not auto-indent every typed newline.
  await page.keyboard.sendCharacter(code);
}

async function runCell(page, index) {
  await page.waitForFunction((selector, i) => {
    const b = document.querySelectorAll(selector)[i];
    return b && !b.classList.contains('disabled');
  }, {timeout: 180000}, run, index);
  // OJS schedules evaluation asynchronously; an enabled button immediately
  // after clicking does not mean the cell has finished. Wait for new output.
  await page.evaluate(i => {
    document.querySelectorAll('.exercise-cell')[i].querySelectorAll('.cell-output-container')
      .forEach(x => { x.dataset.previous = 'true'; });
  }, index);
  await (await page.$$(run))[index].click();
  await page.waitForFunction((selector, i) => {
    const b = document.querySelectorAll(selector)[i];
    const output = document.querySelectorAll('.exercise-cell')[i]
      .querySelector('.cell-output-container:not([data-previous])');
    return output && b && !b.classList.contains('disabled');
  }, {timeout: 90000}, run, index);
}

(async () => {
  // Test real browser HTTP transport without depending on production API CORS.
  // Responses are explicit local fixtures; the small FTP TSV remains a live GET.
  const data = name => JSON.parse(fs.readFileSync(path.join(__dirname, 'fixtures', `${name}.json`)));
  let scenario = 'normal';
  const calls = [];
  const fixtureServer = http.createServer((req, res) => {
    const url = new URL(req.url, 'http://localhost');
    calls.push(url.pathname + url.search);
    let body;
    if (url.pathname.endsWith('/analyses/')) {
      body = scenario === 'empty' ? {count: 0, items: []} : data('analyses');
      const size = Number(url.searchParams.get('page_size') || 20);
      const page = Number(url.searchParams.get('page') || 1);
      body.items = body.items.slice((page - 1) * size, page * size);
    } else if (url.pathname.startsWith('/studies/')) body = data('study');
    else if (url.pathname.startsWith('/analyses/')) {
      body = data('analysis');
      if (scenario === 'missing') body.downloads = [];
    }
    res.writeHead(body ? 200 : 404, {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'});
    res.end(JSON.stringify(body || {detail: 'Not found'}));
  });
  await new Promise(resolve => fixtureServer.listen(0, '127.0.0.1', resolve));
  const fixtureApi = `http://127.0.0.1:${fixtureServer.address().port}`;
  const browser = await puppeteer.launch({headless: true, args: ['--no-sandbox']});
  try {
    for (const language of ['python', 'r']) {
      const page = await browser.newPage();
      await page.setViewport({width: 1440, height: 1000});
      page.on('pageerror', e => {
        if (!e.message.includes('Invalid study accession')) console.error(`${language}: ${e.message}`);
      });
      page.on('console', m => {
        if (m.type() === 'error' && !m.text().includes('Invalid study accession')) {
          console.error(`${language}: ${m.text()}`);
        }
      });
      await page.goto(`${base}/${language}.html`, {waitUntil: 'networkidle2', timeout: 60000});
      assert.equal(await page.$eval('[name=study]', x => x.value), 'MGYS00010393');
      assert.equal(await page.$$eval(run, xs => xs.length), 6);

      const sourceCode = async index => {
        const encoded = await page.evaluate(i => {
          const tag = [...document.querySelectorAll('script')].find(s => s.type === `pyodide-${i+1}-contents` || s.type === `webr-${i+1}-contents`);
          return tag.textContent;
        }, index);
        return JSON.parse(Buffer.from(encoded, 'base64').toString('utf8')).code;
      };
      const setupCode = await sourceCode(0);
      const override = language === 'python' ? `\nAPI = "${fixtureApi}"` : `\nAPI <- "${fixtureApi}"`;
      await editCell(page, 0, setupCode + override);
      scenario = 'normal';
      calls.length = 0;
      for (let i = 0; i < 6; i++) await runCell(page, i);
      assert.ok(calls.some(x => x.includes('page=1&page_size=20')));
      const text = (await Promise.all(page.frames().map(f => f.evaluate(() => document.body?.innerText || '')))).join('\n');
      assert.ok(text.includes('PF00005'), 'live FTP Pfam table must contain the ABC transporter domain');
      assert.ok(!text.includes('Error in '));
      await page.evaluate(() => window.scrollTo(0, 0));
      await page.screenshot({path: `/tmp/mgnify-${language}-simplified.png`, fullPage: true});

      // Check normal editing and execution without custom editor integration.
      const edited = (language === 'python' ? 'print("EDIT_OK")' : 'cat("EDIT_OK")');
      await editCell(page, 5, edited);
      await runCell(page, 5);
      const output = () => page.$$eval('.cell-output-container', xs => xs.map(x => x.innerText).join('\n'));
      assert.ok((await output()).includes('EDIT_OK'));

      await editCell(page, 2, (await sourceCode(2)).replace('page=1', 'page=2'));
      await runCell(page, 2);
      assert.ok(calls.some(x => x.includes('page=2')));
      await editCell(page, 2, await sourceCode(2));
      scenario = 'empty';
      for (const i of [2, 3]) await runCell(page, i);
      assert.ok((await output()).includes('This study has no analyses'));
      scenario = 'missing';
      for (const i of [2, 3, 4]) await runCell(page, i);
      assert.ok((await output()).includes('No Pfam table'));

      await page.goto(`${base}/${language}.html?study=MGYS00005116`, {waitUntil: 'networkidle2'});
      assert.equal(await page.$eval('[name=study]', x => x.value), 'MGYS00005116');
      await runCell(page, 0);
      assert.ok((await output()).includes('MGYS00005116'));
      console.log(`${language}: HTTP, FTP table, pagination, editing, deep links and missing data passed`);

      await page.goto(`${base}/${language}.html?study=invalid`, {waitUntil: 'networkidle2'});
      await page.waitForFunction(() => document.body.innerText.includes('Invalid study accession'));
      await page.close();
    }
  } finally {
    await browser.close();
    await new Promise(resolve => fixtureServer.close(resolve));
  }
})().catch(e => {console.error(e); process.exitCode = 1;});
