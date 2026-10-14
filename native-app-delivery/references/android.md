# Android evidence route

Inspect the actual Gradle project/modules, variants, SDK levels, native/framework
boundaries, dependencies and installed toolchain. Discover supported build/test
commands from trusted project configuration/help. Do not upgrade SDKs or install
emulators implicitly just to turn an unavailable check green.

Distinguish configuration change, activity recreation and process death. Define
saved UI state versus durable data/pending operations and verify recovery from the
actual authoritative store. Review background execution policy, permission denial/
revocation, link/navigation/task behavior, offline state and duplicate delivery.
Do not promise background completion independent of OS policy or client-only
exactly-once business semantics. Verify adaptive layouts, font scale, TalkBack,
keyboard/focus and relevant startup/jank/memory behavior with actual named tooling.
Emulator, device, bundle/signing, test-track processing and production observations
are different layers; retain unavailable checks.

Primary references: [Android core app quality](https://developer.android.com/develop/adaptive-apps/quality-guidelines/core-app-quality)
and [offline-first architecture](https://developer.android.com/topic/architecture/data-layer/offline-first)
(reviewed 2026-10-14). Consult current version-specific guidance before choosing
APIs or background-work behavior. This procedure does not provision Play accounts.
