# Use Case: Health Tracker iOS App

## Request
"Build a health tracking app for iOS using SwiftUI and HealthKit"

## Search Command
```bash
python scripts/search.py "health tracker ios swiftui" --architecture -p "HealthPulse"
```

## Expected Output
```
TARGET: HealthPulse
PLATFORM:   iOS
LANGUAGE:   Swift
UI:         SwiftUI + Charts
ARCH:       MVVM + @Observable (iOS 17+)
NAVIGATION: NavigationStack + TabView + WidgetKit
STATE:      @Observable + async/await
DATABASE:   SwiftData or CoreData
NETWORK:    URLSession async/await
DI:         Manual (Environment) or Swinject
TESTING:    XCTest + swift-snapshot-testing + XCUITest
DEPLOY:     Fastlane deliver + TestFlight
AVOID:      Force unwrapping, Missing accessibility, No dark mode
```
