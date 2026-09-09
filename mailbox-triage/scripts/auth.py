#!/usr/bin/env python3
"""One-time OAuth for a mailbox-triage deployment. Writes token.json next to
the config file (or wherever config.token_path points).

Usage: auth.py [path/to/account.yaml]   (default: ./account.yaml)
"""
import os
import sys

import yaml
from google_auth_oauthlib.flow import InstalledAppFlow

HERE = os.path.dirname(os.path.abspath(__file__))


def load_config(path):
    with open(path) as f:
        cfg = yaml.safe_load(f)
    base = os.path.dirname(os.path.abspath(path))
    for key in ("client_secret_path", "token_path"):
        cfg[key] = os.path.join(base, cfg[key]) if not os.path.isabs(cfg[key]) else cfg[key]
    return cfg


def main():
    config_path = sys.argv[1] if len(sys.argv) > 1 else "account.yaml"
    cfg = load_config(config_path)

    client_secret = cfg["client_secret_path"]
    token_path = cfg["token_path"]
    scopes = cfg["scopes"]

    if not os.path.exists(client_secret):
        raise SystemExit(
            f"Missing {client_secret}. Run setup_wizard.sh first, or download the "
            "OAuth Desktop client JSON from Google Cloud console and save it there."
        )

    flow = InstalledAppFlow.from_client_secrets_file(client_secret, scopes)
    creds = flow.run_local_server(port=0, prompt="consent")
    with open(token_path, "w") as f:
        f.write(creds.to_json())
    print(f"OK — token written to {token_path}. Account '{cfg.get('account')}' is now readable.")


if __name__ == "__main__":
    main()
