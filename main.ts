// The Daily Chronicle - 25 November 2026.
// Entry program: renders the one-page illustrated newspaper (entry.png)
// by running render.py (Python 3 + Pillow, no network, no external assets).
import { spawnSync } from "node:child_process";

const run = spawnSync("python3", ["render.py"], {
  cwd: import.meta.dirname,
  stdio: "inherit",
});
if (run.error) {
  console.error(run.error.message);
  process.exit(1);
}
process.exit(run.status ?? 1);
