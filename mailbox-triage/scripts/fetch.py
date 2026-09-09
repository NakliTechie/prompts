#!/usr/bin/env python3
"""Read-only triage fetch for one mailbox-triage account.

Prints JSON to stdout: threads matching the account's configured queries,
with full plaintext body pulled for anyone on priority_senders. READ-ONLY —
this script never sends, labels, or deletes anything, regardless of the
token's OAuth scope.

Usage: fetch.py [path/to/account.yaml]   (default: ./account.yaml)

Exit codes: 0 = printed results; 2 = not set up yet (no token) — caller
should skip this account silently and note "<account>: not connected".
"""
import base64
import json
import os
import re
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    base = os.path.dirname(os.path.abspath(path))
    for key in ("client_secret_path", "token_path"):
        cfg[key] = os.path.join(base, cfg[key]) if not os.path.isabs(cfg[key]) else cfg[key]
    return cfg


def _plaintext(payload):
    """Recursively extract decoded text from a Gmail message payload."""
    if not payload:
        return ""
    mt = payload.get("mimeType", "")
    data = payload.get("body", {}).get("data")
    if mt == "text/plain" and data:
        return base64.urlsafe_b64decode(data + "==").decode("utf-8", "replace")
    text = ""
    for part in payload.get("parts", []) or []:
        text += _plaintext(part)
    if not text and mt == "text/html" and data:
        html = base64.urlsafe_b64decode(data + "==").decode("utf-8", "replace")
        text = re.sub(r"<[^>]+>", " ", html)
    return text


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "account.yaml"
    cfg = load_config(config_path)

    token_path = cfg["token_path"]
    scopes = cfg["scopes"]
    account = cfg.get("account", "(unnamed account)")
    queries = cfg.get("queries", ["is:unread in:inbox is:important newer_than:2d"])
    priority_senders = [s.lower() for s in cfg.get("priority_senders", [])]
    max_results = cfg.get("max_results_per_query", 25)
    body_char_limit = cfg.get("priority_body_char_limit", 6000)

    if not os.path.exists(token_path):
        print(json.dumps({"connected": False, "account": account,
                          "reason": f"no token at {token_path} — run auth.py once"}))
        sys.exit(2)

    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build

    creds = Credentials.from_authorized_user_file(token_path, scopes)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    svc = build("gmail", "v1", credentials=creds, cache_discovery=False)
    seen, items = set(), []
    for q in queries:
        resp = svc.users().messages().list(userId="me", q=q, maxResults=max_results).execute()
        for m in resp.get("messages", []):
            if m["id"] in seen:
                continue
            seen.add(m["id"])
            full = svc.users().messages().get(
                userId="me", id=m["id"], format="metadata",
                metadataHeaders=["From", "Subject", "Date"]).execute()
            h = {x["name"].lower(): x["value"] for x in full.get("payload", {}).get("headers", [])}
            sender = h.get("from", "")
            item = {
                "id": m["id"],
                "threadId": full.get("threadId"),
                "from": sender,
                "subject": h.get("subject", "(no subject)"),
                "date": h.get("date", ""),
                "snippet": full.get("snippet", "")[:200],
                "matched": q,
            }
            if any(ps in sender.lower() for ps in priority_senders):
                item["priority"] = True
                fullmsg = svc.users().messages().get(
                    userId="me", id=m["id"], format="full").execute()
                item["body"] = _plaintext(fullmsg.get("payload", {})).strip()[:body_char_limit]
            items.append(item)
    print(json.dumps({"connected": True, "account": account,
                      "count": len(items), "items": items}, indent=2))


if __name__ == "__main__":
    main()
