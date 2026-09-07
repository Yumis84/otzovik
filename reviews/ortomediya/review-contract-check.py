#!/usr/bin/env python3
"""Static contract check for the public Ortomediya review page.

The checker is intentionally read-only. It validates the public HTML boundary
and does not connect to Supabase, Cloudflare, or any production service.
"""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles = []
        self.current = None
        self.stack = []
        self.jsonld = []
        self.in_script = False
        self.script_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.stack.append(tag)
        if tag == "article" and attrs.get("class") == "review":
            self.current = {"attrs": attrs, "text": "", "time": None}
        if tag == "time" and self.current is not None:
            self.current["time"] = attrs.get("datetime")
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_script = True
            self.script_text = []

    def handle_endtag(self, tag):
        if tag == "article" and self.current is not None:
            self.articles.append(self.current)
            self.current = None
        if tag == "script" and self.in_script:
            self.jsonld.append("".join(self.script_text))
            self.in_script = False
        if self.stack:
            self.stack.pop()

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data
        if self.in_script:
            self.script_text.append(data)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("reviews/ortomediya/index.html")
    html = path.read_text(encoding="utf-8")
    parser = Parser()
    parser.feed(html)

    required_markers = [
        'rel="canonical"',
        'https://отзыв.com/reviews/ortomediya/',
        'id="reviews"',
        'application/ld+json',
    ]
    for marker in required_markers:
        if marker not in html:
            fail(f"missing required marker: {marker}")

    # Public review pages must not leak private or moderation-only fields.
    forbidden = [
        "author_email",
        "source_ip",
        "turnstile_token",
        "moderation_notes",
        "service_role",
        "SUPABASE_SERVICE_ROLE_KEY",
    ]
    lowered = html.lower()
    for marker in forbidden:
        if marker.lower() in lowered:
            fail(f"private/internal field exposed: {marker}")

    # Prototype is intentionally closed to indexing until real publication is ready.
    if 'name="robots" content="noindex,nofollow"' not in html:
        fail("prototype page must remain noindex,nofollow")

    # No review articles is valid for the current empty public state.
    for i, article in enumerate(parser.articles, 1):
        attrs = article["attrs"]
        review_id = attrs.get("data-review-id", "")
        element_id = attrs.get("id", "")
        if not review_id or not element_id.startswith("review-"):
            fail(f"review #{i}: missing stable Review ID")
        if not article["time"]:
            fail(f"review #{i}: missing time/datetime")
        if not article["text"].strip():
            fail(f"review #{i}: empty visible review content")

    for raw in parser.jsonld:
        try:
            json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(f"invalid JSON-LD: {exc}")

    print(f"PASS: {path} — {len(parser.articles)} published review article(s) satisfy the static boundary checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
