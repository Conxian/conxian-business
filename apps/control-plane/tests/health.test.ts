import assert from "node:assert/strict";
import { test } from "node:test";
import { healthResponse } from "../lib/health";

test("only an explicit successful schema/privilege result is healthy", async () => {
  const response = await healthResponse(async query => {
    assert.equal(query.query_timeout, 2000);
    return { rows: [{ ready: true }] };
  });
  assert.equal(response.status, 200);
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.deepEqual(await response.json(), { status: "healthy" });
});

for (const rows of [[], [{ ready: false }], [{ ready: null }], [{ ready: "true" }],
  [{}], [null], [{ ready: true }, { ready: true }]]) {
  test(`absent or malformed schema result remains unavailable: ${JSON.stringify(rows)}`, async () => {
    const response = await healthResponse(async () => ({ rows }));
    assert.equal(response.status, 503);
    assert.deepEqual(await response.json(), { status: "unhealthy" });
  });
}

test("dependency errors never disclose connection details", async () => {
  const response = await healthResponse(async () => { throw new Error("postgres://private:secret@database/operator"); });
  assert.equal(response.status, 503);
  assert.equal(response.headers.get("cache-control"), "no-store");
  assert.deepEqual(await response.json(), { status: "unhealthy" });
});
