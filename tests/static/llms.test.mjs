import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import test from 'node:test';

const source = await readFile(new URL('../../llms.txt', import.meta.url), 'utf8');

test('llms.txt sections contain linked file lists, with prose in the introduction', () => {
  const [intro, ...sections] = source.split(/^##[ \t]+(.+)$/m);
  assert.match(intro, /^# .+/);
  assert.ok(sections.length > 0, 'Provide links to documentation');

  for (let i = 0; i < sections.length; i += 2) {
    const heading = sections[i];
    const lines = sections[i + 1].split('\n').map(line => line.trim()).filter(Boolean);
    assert.ok(lines.length > 0, `${heading} must contain links`);
    for (const line of lines) {
      const link = line.match(/^-\s+\[[^\]]+\]\((https?:\/\/[^)]+)\)(?::\s*.*)?$/);
      assert.ok(link, `${heading} must contain only linked entries: ${line}`);
      assert.doesNotThrow(() => new URL(link[1]));
    }
  }
});
