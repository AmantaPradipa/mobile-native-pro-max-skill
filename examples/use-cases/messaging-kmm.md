# Use Case: Cross-Platform Messaging App (KMM)

## Request
"Build a messaging app shared between Android and iOS using Kotlin Multiplatform"

## Search Command
```bash
python scripts/search.py "messaging kmm kotlin multiplatform" --architecture -p "ChatSync"
```

## Expected Output
```
TARGET: ChatSync
PLATFORM:   KMM (Android + iOS)
LANGUAGE:   Kotlin (shared) + Swift (iOS UI) + Kotlin (Android UI)
UI:         Jetpack Compose (Android) + SwiftUI (iOS)
ARCH:       KMM shared module + Clean Architecture
NAVIGATION: Compose NavHost (Android) + NavigationStack (iOS) + shared routes
STATE:      KMM-ViewModel + StateFlow + SKIE for Swift
DATABASE:   SQLDelight (multiplatform)
NETWORK:    Ktor Client (multiplatform) + kotlinx.serialization
DI:         Koin (multiplatform)
TESTING:    kotlin.test (shared) + Compose UI Test + XCUITest
DEPLOY:     GitHub Actions (Android + iOS lanes) + Fastlane
AVOID:      GlobalScope, no offline support, missing iOS Flow wrappers
```
