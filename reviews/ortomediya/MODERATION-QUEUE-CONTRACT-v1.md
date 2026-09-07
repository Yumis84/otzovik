# Отзовик — Ortomediya moderation queue contract v1

Status: prototype contract. No production moderation endpoint is enabled by this document.

## Purpose

Define the operator-facing queue that consumes first-party review drafts without exposing private submission data publicly.

## Queue source

`private.own_review_submissions`

Only submissions belonging to an active company and requiring moderation are eligible for the queue.

## Queue item

The moderation UI may display:

- submission ID;
- received timestamp;
- company/profile;
- branch/location when supplied;
- author display name;
- rating;
- review body;
- language;
- consent status/version metadata necessary for moderation verification;
- duplicate/content-risk flags;
- current moderation status.

Private author email and source-IP hash are not displayed unless a separately approved moderation/security workflow requires them.

## Allowed actions

- `approve` → create/update the corresponding public review as `published`;
- `reject` → retain the submission privately and mark it `removed` or another approved non-public state;
- `dispute` → suspend publication/review the case;
- `archive` → retain history without active publication.

There is no automatic publication action.

## Approval requirements

Before `approve`:

1. submission is currently `draft`;
2. company is active;
3. location belongs to company if supplied;
4. required intake validations and consent records are present;
5. no duplicate public review identity/content is introduced;
6. public projection excludes private fields;
7. source/provenance is explicitly first-party;
8. review meaning is preserved;
9. audit record is created.

## Public projection

Approved data is projected into `public.reviews` using the canonical review model. The public review receives a stable review ID and must render through the published-review HTML contract.

The queue must never expose a draft through the public review list.

## Safety gates

- No test/synthetic review may be published.
- No AI-generated replacement text is published as the user's review.
- No aggregate Otzovik rating is recalculated by moderation.
- No production Cloudflare route or Worker traffic change is implied.
- No database mutation is implemented until the real Supabase schema and existing functions have been inspected.

## Next implementation step

Inspect the actual `private.own_review_submissions` table, grants, indexes and existing moderation/publication functions in Supabase project `otzovik`. Then implement the smallest auditable moderation RPC/API surface and verify it with a rollback-safe test.