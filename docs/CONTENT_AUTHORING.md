# Content contract · version 1

This repository contains an independent Chinese causal-inference self-study website. Public learning content belongs in `content/`; source reviews, source media and private working material must remain outside this checkout.

## Ownership and file boundaries

- `content/catalog.json`: nine week-level entries and ordered lesson IDs, counts 10/8/2/4/3/2/3/2/5 = 39. Week 1 starts with theory, then R; this is the independent website's reading order, not a claim about original recording chronology.
- `content/lessons/wNN-lNN.json`: one independently editable lesson per file. Keep IDs stable. Lesson writers may edit only their assigned lesson JSON files.
- `content/schema/lesson.schema.json`: formal JSON schema.
- `src/`: UI, state, math and interactive components. Content writers should not edit it.
- `scripts/build.py`: validates and allowlist-copies public source to `dist/`. No private sibling directories are read by the build.

## Lesson fields

Required: `schemaVersion: 1`, `id`, `week`, `order`, `title`, `summary`, `status`, `readingMinutes`, `tags`, `objectives`, `prerequisites`, `sections`, `references`, `exerciseIds`, `codeStatus`.

`status` is `outline`, `draft`, `demo`, or `ready`. `ready` requires completed source and scientific review by the owner, not merely writing. `demo` is an original limited example, not a completed source-course lesson. `readingMinutes` is an original article's estimated reading time, never the source recording duration. `codeStatus` is `none`, `not-run`, or `verified`; the last requires actual execution evidence. Optional `statusNote` explains a material scope limit. `exerciseIds` lists stable exercise IDs used in the lesson.

`sections` is an array of `{id, title, blocks}`. Each block is one of:

- `{type: "paragraph", text}`: plain text, HTML escaped.
- `{type: "list", items: [text], ordered?: boolean}`.
- `{type: "callout", title, text, tone?: "note" | "warning"}`.
- `{type: "equation", text, mathml?, caption?}`. Text is the accessible plain-text fallback. Optional MathML is sanitized with an explicit safe-tag/attribute allowlist, then rendered natively; no CDN dependency.
- `{type: "table", headers: [text], rows: [[text]], caption?}`.
- `{type: "code", language, code, execution: "not-run" | "verified", caption?}`. Use only original code. State the execution status accurately.
- `{type: "exercise", id, prompt, options: [text], answer: zeroBasedIndex, explanation}`. Prefer a concrete objective check, 2–5 alternatives. Answers are intentionally client-visible; this is a self-study tool.
- `{type: "interactive", kind: "standardization"}`. New interactive types require UI implementation and tests first.
- `{type: "diagram", kind: "confounding-dag", caption?}`. New diagram types require UI support.

References: `{id, title, authors, year, url, locator}`. Only actual, relevant primary sources; use HTTPS links and a chapter/section locator where possible. They describe scholarly provenance, not private course files. Do not attach or reproduce source PDFs, recordings, transcripts, screenshots, source-course data or identities. New figures, examples, data and code must be independently authored. Never include local paths, review ledgers, internal source IDs, credentials or personally identifying data.

## Current publication

All 39 lessons have authored bodies, examples, references and self-checks (82 questions in total). `w02-l04` also contains the two-stratum standardization interactive. Content readiness and code execution are separate: 18 Python blocks have execution evidence; all 65 R blocks remain `not-run`. Do not change an execution label merely because the article is ready. Preserve useful limitations when editing status notes.

Lessons retain individual bookmark and completion actions. The application also supports `outline` entries for future additions; completion is disabled for those entries. Keep status labels accurate when adding or revising lessons.

## Validation

Run `npm test` and `npm run build`. Open `dist/` via HTTP (`npm run dev`) rather than `file://`. The built app uses relative asset paths and hash routes, so it can live at `/repo-name/` on GitHub Pages. The Pages workflow tests and builds on `main` changes, then uploads only `dist/`. Review all changes for scientific accuracy, execution labels and publication suitability before merging.
