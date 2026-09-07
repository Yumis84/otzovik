# Review Pipeline v1

## Current state

The public review page is currently a noindex structural prototype. It must not contain fabricated or placeholder reviews presented as real content.

The canonical review data model now uses `public.reviews.body` for the full permitted review text. `excerpt` is retained for compatibility/summary use.

## Publication contract

A review may become public only after:

1. a real submission or otherwise permitted source record exists;
2. provenance is recorded;
3. company and optional branch/location are linked;
4. moderation/publication rules are satisfied;
5. the review is stored with `status = published`;
6. the public profile RPC exposes the published review;
7. the rendered public HTML contains the full permitted text and stable review identifier.

## External sources

External review text must not be copied into public pages until the applicable technical and legal permission/terms have been verified. External source ratings remain separate from Otzovik.com reviews.

## Next implementation

Build the public review renderer against the `get_public_company_profile_v2` response, then perform one end-to-end test with a real permitted review. Do not seed fake review data merely to make the page look populated.
