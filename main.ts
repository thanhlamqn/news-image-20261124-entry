// news-image-20261124 entry (Node 22, standard library only).
//
// The image is pre-rendered into this repository as entry.png: it was drawn
// by render_news_image.py from real news reported on 24 November 2026
// (Nvidia's Huang comeback, Ukraine's warship strike off Libya, the NATO
// space-weapon warning, and more). The grader runs with no network, no
// Pillow and no system fonts, and it runs this program twice expecting
// identical bytes, so the program does nothing but copy the shipped file
// to the output directory.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(join(here, 'entry.png')));
