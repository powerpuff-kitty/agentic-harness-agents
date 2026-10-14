---
name: native-app-delivery
description: "Implement and verify scoped iOS/Android app changes across lifecycle, durable state, offline behavior, permissions, deep links, adaptive UI and release preparation. Use for native/mobile delivery including cross-platform shells; do not treat responsive web or a simulator-only pass as real-device/store verification."
---
# Native App Delivery

## Objective and inputs

Deliver the accepted app behavior with platform-specific evidence. Establish target
project/platforms, stack/build configuration, user journey, supported OS/device range,
permissions, actual toolchain and change/release scope. Do not infer that the current
working directory or a public marketing site is the target app.

## Procedure

1. Inspect project/build files and available tool versions; identify native modules,
   storage/network boundaries, app lifecycle and target devices. Use the [method](references/method.md)
   plus only the relevant [iOS](references/ios.md) or [Android](references/android.md)
   guide. React Native/Flutter or other shells still need platform-specific checks.
2. Map startup/resume, process/activity recreation, background work, deep links,
   navigation/back behavior, permissions and offline/pending/error states to accepted
   behavior. Define durable versus transient state and pending-operation ownership.
3. Design and implement the smallest authorized change using existing architecture
   and dependencies. Preserve user work; do not add unrequested persistence, tracking,
   background collection, backend services or production configuration.
4. Define offline read/write policy, retries/idempotency, auth expiry, conflict and
   sync recovery with source/business guarantees. Distinguish restored UI from
   durable business completion; do not promise exactly-once delivery from a UI queue.
5. Verify actual build/test targets and relevant lifecycle, denied/revoked permission,
   process death, connectivity loss, duplicate delivery, deep-link and text/theme/
   orientation/adaptive states. Accessibility and performance need appropriate native
   tools and actual evidence; screenshots do not prove semantics or energy budgets.
6. Separate static review, unit tests, simulator/emulator, real-device and signed
   distribution checks. Record OS/SDK/device/build identity and unavailable layers.
   Missing SDK/hardware/credentials is not a passing result or automatic install scope.
7. Prepare release/version/signing/privacy/capability evidence when requested; route
   actual distribution to the existing approved release workflow. No account change,
   store upload, purchase or production release is granted by implementation alone.
8. Deliver the [app change report](assets/report-template.md), actual artifacts and
   verification matrix, recovery/compatibility gaps and handoff. Use current primary
   platform docs for concrete APIs/entitlements/toolchain commands, not guessed calls.

## Completion

Requested behavior is implemented or the precise capability blocker is documented;
source/build/device/distribution claims remain distinct. Required project checks and
real tested states are reported without claiming unobserved platform coverage.
