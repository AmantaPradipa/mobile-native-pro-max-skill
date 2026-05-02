# Mobile-Native Pro Max — Dataset Reference

## Domain CSVs

Each domain CSV follows the standard column format:
`id,category,name,description,when_to_use,trade_offs,implementation_notes,keywords,references`

### UI Components (`ui_components.csv`)
Patterns for Bottom Navigation, RecyclerView/LazyColumn, Bottom Sheets, Forms, Cards, Toolbars, Snackbars, FABs, Chips, Skeleton Screens, Empty States, Pull-to-Refresh, Search Bars, and Segmented Controls.

### Navigation Patterns (`navigation_patterns.csv`)
Stack Navigation, Tab Navigation, Drawer, Deep Linking, Modal, Safe Args, Predictive Back, Nested Graphs, Auth-Gated Navigation, Result/Callback, Animations, and Navigable Bottom Sheets.

### Architecture Patterns (`architecture_patterns.csv`)
MVVM, MVI, Clean Architecture, Multi-Module, Repository Pattern, Dependency Injection, Coordinator/Router, Offline-First, Reactive Streams, KMM, Compose Multiplatform, and SwiftUI + Swift Concurrency.

### State Management (`state_management.csv`)
ViewModel State, StateFlow/Observation, Side Effects, Paging, Form State, Loading/Error/Success, Process Death, Shared State, Undo/Redo, Offline Sync Queue, Cache Invalidation, and KMM Shared State.

### Performance Optimization (`performance_optimization.csv`)
Startup, Memory, Rendering (60fps), Network, Battery, Image Loading, Compose Recomposition, ProGuard/R8, Database, Animation, Startup Tracing, and Lazy Initialization.

### Testing Strategies (`testing_strategies.csv`)
Unit Tests, UI Tests, Screenshot/Snapshot Tests, Integration/E2E, ViewModel Testing, Repository Testing, Accessibility Testing, Benchmarks, Network/API Contract, Leak Detection, Concurrency Tests, and Compose Preview Screenshot Tests.

### Platform APIs (`platform_apis.csv`)
Camera, Location/Geofencing, Push Notifications, Biometric Auth, Storage/Keychain, Runtime Permissions, Bluetooth LE, Home Screen Widgets, Share/Intents, In-App Purchases, Accessibility APIs, and App/Universal Links.

### Build & Deployment (`build_deployment.csv`)
Play Store, App Store, Fastlane, GitHub Actions, Code Signing, Versioning, Build Flavors/Schemes, Beta Distribution, Crash Reporting, Feature Flags, App Size Monitoring, and Dependency Security Scanning.

## Anti-Patterns (`anti_patterns.csv`)
25 mobile-specific anti-patterns from CRITICAL to MEDIUM severity covering main-thread violations, missing error handling, hardcoded secrets, memory leaks, god activities, missing ProGuard, lifecycle violations, and more.

## Technology Stacks (`stacks.csv`)
24 technology stacks: Kotlin, Swift, Java, Objective-C, Dart, Jetpack Compose, SwiftUI, UIKit, Flutter, KMM, Compose Multiplatform, Room, CoreData, SQLDelight, Retrofit, Ktor, Alamofire, Hilt, Koin, Firebase, Fastlane, Gradle, Xcode/SPM, and Coil.
