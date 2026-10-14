# Browser, visual and recovery evidence

Load for meaningful browser-state coverage, visual regression or recovery tests.
Define the accepted behavior before choosing a screenshot baseline or fault model.

## Browser and visual matrix

Select representative route/journey, viewport/device scale, browser/version, locale,
theme, input method and component states. Include relevant loading/empty/error,
permission and long-content cases; do not multiply every dimension mechanically.
Record the tested subset and exclusions. A screenshot of an error route is not a
passing checkout, even if it exactly matches an accidentally accepted error baseline.

Wait for observable product state, not universal network-idle or an arbitrary sleep.
Confirm route/content/state, font/assets and animation conditions before capture.
Keep environment, fonts, data and clock deterministic where supported; identify
dynamic content and justify any masks/normalization. Do not mask the feature under
test, hide a failing state or increase tolerances to erase a real defect.

Tie screenshots to named behavior assertions and a versioned reviewed baseline.
Inspect visual changes, unexpected baseline creation and missing screenshots.
Do not auto-approve new reference images merely to make CI pass. A diff threshold
is an engineering policy with scope, not proof of perceptual or accessibility quality.
Retain retry failures and traces/screens of the failed attempt; a later green retry
does not establish reliability. Browser evidence does not prove native-app semantics.

## Recovery scenarios

Use a scoped isolated fault model: timeout, lost response, connectivity loss, process
restart, retry, expired permission/auth, interrupted write or dependency failure.
Specify what was acknowledged, what is durably committed, ownership/idempotency,
expected recovery state and bounds. A saved toast or queued in-memory operation
does not prove survival after restart. Verify no lost acknowledged state, duplicate
business action, cross-user leakage or irrecoverable navigation where required.

Reproduce the fault and observe restoration and user-visible recovery using actual
tools. Record injection point, target/build/environment, time boundaries, persisted
state, duplicates and failures. If no executable fixture exists, deliver a plan or
source-supported finding; do not claim a recovery test passed. Live production fault
injection, service shutdown, data mutation or restoration needs actual separate scope.

Primary browser reference: [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots)
(reviewed 2026-10-14). Discover current runner APIs locally before authoring code;
these instructions do not install a runner or prescribe one for every project.
The [synthetic evidence fixture](../tests/fixtures/browser-recovery.json) is a review
exercise, not a browser trace, approved baseline or actual recovery measurement.
