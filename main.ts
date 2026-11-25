// The Daily Chronicle - 25 November 2026.
// Entry program: delivers the one-page illustrated newspaper to the
// grader's output directory. The image itself (entry.png, 1024x1024)
// was rendered beforehand by render.py (Python 3 + Pillow, no network,
// no external assets) and is committed in this repository; this file
// only places a copy where the grader looks for it.
//
// Why a copy and not a render: the grader runs this file as
// `node /bot/main.ts` in a Node-only image, on a read-only copy of the
// repository, with no Python, no Pillow and no system fonts. Rendering
// here would fail at the first missing piece, so the render step lives
// outside the graded run and this file stays pure Node stdlib.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = new URL("./entry.png", import.meta.url);

try {
  mkdirSync(outDir, { recursive: true });
  copyFileSync(source, join(outDir, "entry.png"));
} catch (err) {
  console.error("could not deliver entry.png:", err.message);
  process.exit(1);
}

console.log("entry.png delivered to", join(outDir, "entry.png"));
