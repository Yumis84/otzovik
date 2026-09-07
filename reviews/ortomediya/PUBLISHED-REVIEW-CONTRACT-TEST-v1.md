# Published Review Contract Test v1

Status: prototype / QA contract. This file does not publish, modify, or fabricate reviews.

## Purpose

Validate a future published review object against the Отзыв.com public HTML contract before it becomes visible on the public review page.

## Required visible HTML

A published review must render as an ordinary HTTP-delivered semantic HTML article:

- `<article class="review" id="review-<stable-review-id>" data-review-id="<stable-review-id>">`
- author name in a heading
- rating as visible text on a 1–5 scale and an accessible label
- publication date in `<time datetime="...">`
- company/location context when applicable
- review body as ordinary text
- provenance/source information
- optional company response only when it is an actual retained response
- separate complaint/report action where implemented

Mandatory review content must not depend on client-side JavaScript.

## JSON-LD consistency

If Review JSON-LD is present, the test must compare it with the visible HTML for at least:

- stable review identifier
- author display name
- rating value and scale
- publication date
- review body
- company identity
- provenance/source where represented

A JSON-LD value that is absent from or contradicts visible content is a failure.

## Publication safety gates

Fail the test if any of these conditions are detected:

1. status is not `published`;
2. Review ID is missing or unstable;
3. author private email is exposed;
4. raw IP or internal moderation fields are exposed;
5. review text is fabricated, synthetic, or a test fixture;
6. review meaning was rewritten during publication;
7. provenance is missing for a first-party or external review;
8. rating is outside 1–5 or has no declared scale;
9. publication date is missing/invalid;
10. mandatory content exists only in JavaScript state;
11. JSON-LD contradicts visible HTML;
12. a draft/removed/disputed/archived record is exposed publicly;
13. publication creates an aggregate Отзыв.com rating without an approved separate decision.

## First-party publication mapping

For a first-party submission, the publication layer may copy only the approved public fields:

`company_id`, `location_id`, first-party source identifier, `author_display_name`, `published_at`, `rating`, `rating_scale`, approved review body, `language`, `content_hash`, `provenance`, `status`.

Private email, raw IP, Turnstile token, honeypot value, consent internals, moderation notes and internal audit data remain private.

## Test fixture policy

Synthetic fixtures may be used only in non-public automated tests. They must never be inserted into the production public review list or used as a real review example.

## Execution gate

The test becomes executable against the real publication path only after the Supabase schema and publication function are inspected and the protected moderation path exists. No production Cloudflare/DNS changes are part of this contract.

## Expected result

`PASS` only when the complete published object, rendered HTML and optional JSON-LD agree and no private/moderation-only data crosses the public boundary.
