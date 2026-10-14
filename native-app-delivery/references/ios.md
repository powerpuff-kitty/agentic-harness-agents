# iOS evidence route

Inspect the actual project/workspace, deployment target, schemes/configurations,
Swift/Objective-C or cross-platform/native boundary and installed Xcode/SDK. Discover
commands/targets with trusted local help/project settings before building; do not
invent signing identities or expose provisioning credentials.

Verify scene/app lifecycle, state restoration and persistence separately; process
termination is not a reliable opportunity to save critical pending work. Evaluate
background capabilities against the actual OS/entitlements and task, not an assumed
unlimited worker. Review permission denial/revocation, URL/universal-link entry,
secure storage, network transitions and interrupted operations with actual APIs.
Use relevant accessibility, text scaling, VoiceOver, orientation/window and performance
checks on named targets. Simulator observations and device/beta/store evidence remain
distinct. App privacy/signing/account requirements depend on the actual release scope.

Primary route: [Apple beta/release distribution](https://developer.apple.com/documentation/xcode/distributing-your-app-for-beta-testing-and-releases/)
(accessed 2026-10-14). Consult the current Apple API documentation for the concrete
lifecycle/storage/background capability; this guide does not pin an SDK or authorize
store actions. No Apple toolchain is required to produce an honest planning report.
