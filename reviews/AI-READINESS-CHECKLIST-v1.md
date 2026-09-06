# Отзыв.com — Review AI / Search Readiness Checklist v1

## Purpose
Проверить, что опубликованный отзыв доступен человеку, поисковому роботу и AI-агенту из одного канонического HTML-представления.

## Required publication contract
- [ ] Review is present in ordinary HTTP-delivered HTML.
- [ ] Review text does not require JavaScript to become readable.
- [ ] Stable `review-<id>` identifier exists.
- [ ] Author display name is explicit.
- [ ] Rating is explicit as `N из 5` and exposed accessibly.
- [ ] Publication date uses `<time datetime="...">`.
- [ ] Company context is explicit.
- [ ] Branch/service is shown only when supported by stored evidence.
- [ ] Provenance/source is explicit.
- [ ] External-source text is published only when republication is permitted.
- [ ] Company response, if present, is visibly attached to the review.
- [ ] Complaint action does not silently alter the review.

## Search-engine checks
- [ ] Canonical URL is correct.
- [ ] `robots.txt` permits intended public crawling.
- [ ] Sitemap contains canonical public profile/review URLs.
- [ ] No accidental `noindex` on production review pages.
- [ ] No review content is hidden only in client-side state.
- [ ] JSON-LD, when used, matches visible HTML exactly.
- [ ] No fabricated ratings, review counts, authors, dates or text.

## AI-agent checks
- [ ] Agent can extract company, review ID, author, rating, date and body from HTML.
- [ ] Agent can distinguish first-party and external provenance.
- [ ] Agent can trace a summary claim back to specific Review IDs.
- [ ] Freshness/publication date is machine-readable.
- [ ] Missing or uncertain fields remain missing/uncertain rather than inferred as facts.
- [ ] AI Summary is an analysis layer and never replaces the underlying review evidence.
- [ ] No unsupported recommendation or competitor-comparison language is generated.

## Raw HTTP acceptance test
Use a production-like URL and verify the response body directly, without executing browser JavaScript. Extract:
1. `article.review`
2. stable review ID
3. author
4. rating
5. publication date
6. full permitted body
7. provenance
8. company response if present

The test passes only when these values are recoverable from the HTML response and agree with the canonical review record.

## Current prototype status
GitHub-first. This checklist is documentation/QA only. No Cloudflare or production publication is enabled by this file.
