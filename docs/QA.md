# Verification scope

Publication snapshot: 2026-10-04 UTC.

## Automated checks

- JavaScript syntax: application, math and state modules.
- 10 Node tests: standardization, all 101 target weights, endpoints, invariant crude difference, malformed weights, display units, known-ID state validation, blocked/corrupt storage helpers, reversible bookmarks and bilingual search.
- Content: nine weeks, 39 unique ordered lessons, expected chapter counts, full JSON Schema, unique section/exercise IDs, 82 matching exercises, answer indexes, table dimensions, supported blocks and execution-status labels.
- Build: an explicit asset allowlist creates eight public files. The workflow uploads only this `dist/` directory.
- Original code: 18 Python blocks executed independently; 65 R blocks statically reviewed but not executed. Static review does not establish numerical reproduction or package compatibility.

These checks are separate from live browser inspection and do not guarantee the absence of future defects.

## Browser check list

Recheck the deployed GitHub Pages URL after every material UI change:

- All nine chapters and 39 lesson routes; next/previous lesson navigation
- Search, literal special characters, Escape, close and reopen
- Bookmarks, reading progress and self-check persistence after reload
- Empty, incorrect and correct self-check submissions
- Code copy and the text-selection fallback when clipboard access is unavailable
- Standardization slider endpoints and reset
- Direct hash links, unknown routes, Back and Forward
- Desktop and narrow/mobile layout, menu open/close, no horizontal page overflow
- Native MathML layout and readable fallback equations
- Keyboard focus, 200% enlargement, reduced motion and screen-reader behavior
- Browser errors and all eight public assets loading successfully

## Recheck commands

```sh
npm test
npm run build
node --check src/app.js
node --check src/math.js
node --check src/state.js
python3 tests/browser_smoke.py
```

The optional Chromium fixture suite requires Python Playwright and a Chromium installation with permitted process/IPC access. It serves the local public build at a synthetic test origin and does not establish deployment. A blocked or unrun fixture must not be reported as passed. Full screen-reader and assistive-technology testing remains a separate manual activity.
