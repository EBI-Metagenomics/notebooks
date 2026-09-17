import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import test from 'node:test';

const source = await readFile(new URL('../../src/examples/study-link.js', import.meta.url), 'utf8');
const {readStudyAccession} = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);

test('default accession, deep links and legacy alias', () => {
  assert.equal(readStudyAccession(''), 'MGYS00010393');
  assert.equal(readStudyAccession('?study=MGYS00005116'), 'MGYS00005116');
  assert.equal(readStudyAccession('?jlvar_MGYS=MGYS00005116'), 'MGYS00005116');
  assert.equal(readStudyAccession('?study=%20mgys00010393%20'), 'MGYS00010393');
});

test('invalid accessions are rejected', () => {
  for (const query of ['?study=', '?study=MGYS123', '?study=%22%3Bprint(1)']) {
    assert.throws(() => readStudyAccession(query));
  }
});
