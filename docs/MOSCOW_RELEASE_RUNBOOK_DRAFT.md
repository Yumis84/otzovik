# Moscow migration release runbook (DRAFT)

Scope: отзыв.com (xn--b1ajuq0c.com) apex/www, cabinet, and wildcard public profiles. This document is a proposal only. No production deployment is authorized.

## Preconditions

1. Confirm separate Apache virtual hosts and filesystem permissions; do not modify the existing Kaliningrad website.
2. Choose independent DNS provider with API-based DNS-01 support for wildcard TLS. Export and verify the complete current DNS zone, including TXT, MX, CAA and DNSSEC settings.
3. Prepare and validate apex, www and wildcard certificates before changing DNS.
4. Inventory Supabase Auth redirect URLs and all absolute GitHub Pages links; obtain separate approval before changing production Auth.
5. Confirm release artifacts contain only public assets; check checksums and manifests. No credentials in artifacts.
6. Test with explicit Host header and staging access before any DNS changes. Check HTTP 200, 301, 404, 410, security headers, canonical tags, sitemap and robots.
7. Confirm a rollback owner, an on-call window and the exact previous release identifier.

## Proposed immutable release layout

Use a dedicated application directory, for example /srv/otzovik/releases/<release-id>, with distinct subdirectories for site, cabinet and profiles. Keep a stable /srv/otzovik/current symlink pointing to a verified release. Do not share directories or permissions with the Kaliningrad website. Create release in a temporary location, verify integrity, then switch the symlink atomically only after explicit deployment approval.

## Release procedure (NOT AUTHORIZED TO EXECUTE)

1. Build versioned artifacts in CI; publish SHA-256 manifest.
2. Transfer to a staging area with least-privilege credentials.
3. Verify checksums, ownership, content types, absence of secrets and expected entrypoints.
4. Run Apache syntax checks and staging smoke tests; verify default vhost isolation.
5. After separate approval, switch current release and reload Apache gracefully.
6. Verify apex, www, cabinet login flow, profile routes, 404/410, SEO and certificate renewal.
7. Only after stable staging and explicit approval, coordinate DNS/NS cutover with registrar owner. Keep rollback records and monitor errors.

## Rollback procedure (NOT AUTHORIZED TO EXECUTE)

1. Stop rollout on failing smoke tests or unexpected 5xx, certificate or authentication errors.
2. Restore previous current symlink and gracefully reload Apache.
3. If DNS was already changed, coordinate DNS rollback with registrar owner, accounting for TTL and cache propagation.
4. Verify previous release, preserve logs, document incident and avoid destructive cleanup.

## Open blockers

- Final DNS provider and authoritative zone export not confirmed.
- Wildcard certificate issuance and renewal path not validated on Moscow host.
- Full staging environment and server-side smoke tests not performed.
- Supabase Auth redirect changes require separate approval.
- Profile publication and cabinet release integration require independent review.
- Production writes, deployment, main merges and DNS cutover are prohibited until explicit approval.

## Mandatory cutover gates from independent review

- Plan DNS TTL reduction at least 48 hours before the cutover; verify DS/DNSSEC at the registrar before changing authoritative NS. DNS caches can outlive a rollback, so reverting NS is not an instant recovery mechanism.
- Keep the old hosting path available during the stabilization window (target 14 days) and test a canary staging hostname before changing production DNS.
- Supabase Auth: add and test new redirect URLs on staging before cutover, preserve existing redirect URLs during transition, and expect users to sign in again after the origin changes. Any production Auth configuration requires separate approval.
- Maintain three independent immutable release tracks and current pointers: apex, cabinet, and public profiles. Roll back one component without rolling back the others.
- Preserve the existing Kaliningrad Apache vhosts and certificates. Compare httpd -S and representative responses before and after any future approved deployment.
- Require independent smoke checks for wildcard profiles, inactive/tombstone 410 routes, canonical URLs, security headers and cabinet authentication.
