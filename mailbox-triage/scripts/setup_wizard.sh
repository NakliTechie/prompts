#!/usr/bin/env bash
# Interactive setup for ONE local-OAuth mailbox account (the tier-2 path —
# use this only for an account claude.ai's native Gmail connector can't
# reach, e.g. a second Google Workspace domain). Minimizes the manual
# Google Cloud console clicks and scripts everything gcloud can reach.
set -euo pipefail
cd "$(dirname "$0")/.."   # repo-relative: mailbox-triage/

DEPLOY_DIR="${1:-}"
if [ -z "$DEPLOY_DIR" ]; then
  echo "Usage: scripts/setup_wizard.sh <deployment-dir>" >&2
  echo "  e.g. scripts/setup_wizard.sh ~/Code/inbox-watch/office" >&2
  exit 1
fi
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

echo "== mailbox-triage setup: $DEPLOY_DIR =="
echo

read -rp "Google account to watch (e.g. name@yourcompany.com): " ACCOUNT
DOMAIN="${ACCOUNT#*@}"
CRED_HOME="$HOME/.mailbox-triage/credentials"
mkdir -p "$CRED_HOME"
DOMAIN_CLIENT="$CRED_HOME/$DOMAIN.json"

if [ -f "$DOMAIN_CLIENT" ]; then
  echo "Found an existing OAuth client for domain '$DOMAIN' at $DOMAIN_CLIENT."
  echo "Reusing it — no new Google Cloud project needed for this mailbox."
  cp "$DOMAIN_CLIENT" client_secret.json
else
  echo "No OAuth client on file for domain '$DOMAIN' yet. First mailbox in this"
  echo "domain needs a one-time Google Cloud setup (~3 console clicks below)."
  echo

  PROJECT_ID="mailbox-triage-$(echo "$DOMAIN" | tr '.' '-')"
  if command -v gcloud >/dev/null 2>&1; then
    echo "-- gcloud found, scripting what it can reach --"
    if ! gcloud projects describe "$PROJECT_ID" >/dev/null 2>&1; then
      echo "Creating project $PROJECT_ID ..."
      gcloud projects create "$PROJECT_ID" --name="mailbox-triage ($DOMAIN)"
    else
      echo "Project $PROJECT_ID already exists, reusing it."
    fi
    echo "Enabling Gmail API ..."
    gcloud services enable gmail.googleapis.com --project="$PROJECT_ID"
    if gcloud services list --enabled --project="$PROJECT_ID" 2>/dev/null | grep -q gmail.googleapis.com; then
      echo "Confirmed: Gmail API is enabled on $PROJECT_ID."
    else
      echo "WARNING: could not confirm Gmail API is enabled — check the console link below." >&2
    fi
  else
    echo "gcloud CLI not found (skip this by installing it: brew install google-cloud-sdk)."
    echo "You'll create the project by hand at the link below instead."
    read -rp "Google Cloud project ID to use/create (e.g. $PROJECT_ID): " PROJECT_ID
  fi

  echo
  echo "Three manual console steps remain (Google requires a human for these):"
  echo
  echo "1. OAuth consent screen — choose 'Internal' (this domain only):"
  echo "   https://console.cloud.google.com/apis/credentials/consent?project=$PROJECT_ID"
  echo
  echo "2. Create OAuth client — Application type: Desktop app:"
  echo "   https://console.cloud.google.com/apis/credentials?project=$PROJECT_ID"
  echo
  echo "3. Download the client JSON from the credential you just created,"
  echo "   and save it as: $DOMAIN_CLIENT"
  echo
  read -rp "Press Enter once step 3 is done (the file exists at that path) ... " _

  if [ ! -f "$DOMAIN_CLIENT" ]; then
    echo "Still don't see $DOMAIN_CLIENT — re-run this script once it's there." >&2
    exit 1
  fi
  cp "$DOMAIN_CLIENT" client_secret.json
  echo "Saved. Every future mailbox in '$DOMAIN' skips steps 1-3 entirely."
fi

echo
echo "-- local venv + deps --"
python3 -m venv .venv
./.venv/bin/pip install -q --upgrade pip
./.venv/bin/pip install -q -r "$(dirname "$0")/../requirements.txt"

cat > account.yaml <<EOF
account: $ACCOUNT
client_secret_path: client_secret.json
token_path: token.json
scopes:
  - https://www.googleapis.com/auth/gmail.modify   # read+send; fetch.py only reads
queries:
  - "is:unread in:inbox is:important newer_than:2d"
  - "is:unread in:inbox category:primary newer_than:1d"
priority_senders: []
max_results_per_query: 25
priority_body_char_limit: 6000
EOF
echo "Wrote account.yaml — edit priority_senders / queries as needed."

echo
echo "-- authorize (opens a browser — consent as $ACCOUNT) --"
./.venv/bin/python "$(dirname "$0")/auth.py" account.yaml

echo
echo "-- smoke test --"
./.venv/bin/python "$(dirname "$0")/fetch.py" account.yaml
