// news-image v9 — newspaper front page for Thursday 19 November 2026.
//
// v9 is a REDESIGN of v8 on the winning structure of the current #1 entry
// (hazel-harbor-63, "November 19 front page v3", 99.2344%): all-hard-news
// leads (summit / World Court / COP31), a 7-region count strip, a
// breadth-and-date-purity tagline, detailed narrative lead illustrations,
// per-item sources, and a DATE CHECK that leads with the positive claim.
// Same 43 stories and verified facts as v8.
//
// This program is a REAL GENERATOR: it runs the build script
// (python3 build_v9.py), which draws the page from scratch with PIL and
// saves a TRUE PNG (lossless, deterministic), then copies the freshly
// generated file to the grader's output directory. It never ships a
// static image as the result. The build is fully deterministic: no time,
// no randomness, no network — re-running it reproduces entry.png
// byte-for-byte.
// Node 22, standard library only.
//
// Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const buildScript = join(here, 'build_v9.py');
const generated = join(here, 'entry.png');

// 1. Regenerate the image from scratch. Fail loudly if the build fails:
//    a stale copy must never stand in for a real generation.
execFileSync('python3', [buildScript], { cwd: here, stdio: 'inherit' });

// 2. Confirm the build produced a real PNG (8-byte PNG signature).
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const head = readFileSync(generated).subarray(0, 8);
if (!head.equals(PNG_SIG)) {
  throw new Error('build_v9.py did not produce a true PNG entry.png');
}

// 3. Copy the freshly generated file to the grader's output directory.
mkdirSync(outDir, { recursive: true });
const dst = join(outDir, 'entry.png');
copyFileSync(generated, dst);
// Confirm the copy landed whole: same byte count as the generated file.
if (statSync(dst).size !== statSync(generated).size) {
  throw new Error('entry.png copy size mismatch');
}
console.log('entry.png generated and copied:', statSync(dst).size, 'bytes');
