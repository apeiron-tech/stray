#!/usr/bin/env bash
# A disposable local database, with no dotenv file or external provider configuration.
# The port comes from frontend/playwright.config.ts, which picks a free one for each run.
set -euo pipefail
: "${STRAY_E2E_PORT:?set by frontend/playwright.config.ts (or export one to run this by hand)}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/stray-browser.XXXXXX")"
trap 'rm -rf "$TEST_DIR"' EXIT
cd "$TEST_DIR"
export STRAY_DATABASE_URL="sqlite+aiosqlite:///$TEST_DIR/test.db"
export STRAY_PUBLIC_URL="http://127.0.0.1:$STRAY_E2E_PORT"
export STRAY_EMAIL_DEV_MODE=true
export STRAY_FRONTEND_DEV=false
export STRAY_PROMO_GRANT_MICRO=0
export STRAY_RESEND_API_KEY=
export STRAY_POSTHOG_KEY=
export STRAY_INTERCOM_APP_ID=
export STRAY_PLATFORM_PROVIDERS=
# The first-run flow for these addresses only (e2e/onboarding.spec.ts); everyone else, and so every
# other spec's signIn, keeps the team-name dialog.
export STRAY_ONBOARDING_V2_EMAILS=@onboarding.test
export PORT="$STRAY_E2E_PORT"
export STRAY_SECRET_KEY="$(uv run --project "$ROOT" python -m stray keygen)"
export STRAY_SESSION_SECRET=local-disposable-browser-tests
uv run --project "$ROOT" python -m stray
