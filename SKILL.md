---
name: mobile-native-pro-max
description: >
  AI-powered intelligence for native mobile app development across Android (Kotlin/Compose),
  iOS (Swift/SwiftUI), and cross-platform (KMM/Flutter/Compose Multiplatform). Provides
  architecture patterns, navigation strategies, state management, platform API integration,
  performance optimization, testing strategies, build/deployment automation, and anti-pattern
  review for production-grade mobile applications.

  Trigger phrases: build mobile app, android project, ios app, kotlin compose, swiftui,
  flutter app, kmm multiplatform, mobile architecture, buatkan aplikasi mobile, buat app android,
  buat app ios, navigasi mobile, state management mobile, deploy ke play store, deploy ke app store
---

# Mobile-Native Pro Max

## Activation

This skill activates when the user requests:
- Build a mobile app / android project / ios application
- Kotlin Compose architecture / SwiftUI patterns
- Flutter or KMM cross-platform setup
- Mobile navigation / state management
- Performance optimization for mobile
- Play Store / App Store deployment
- Buatkan aplikasi mobile / buat app android / buat app ios

## Step 1: Analyze Request

```bash
python scripts/search.py "<request>" --architecture -p "<Project Name>"
```

## Step 2: Domain-Specific Searches

```bash
# UI component patterns
python scripts/search.py "bottom navigation tab bar" --domain ui-components

# Navigation strategies
python scripts/search.py "deep linking stack navigation" --domain navigation-patterns

# Architecture decisions
python scripts/search.py "clean architecture mvvm" --domain architecture-patterns

# State management
python scripts/search.py "stateflow viewmodel" --domain state-management

# Performance
python scripts/search.py "startup optimization compose" --domain performance-optimization

# Testing
python scripts/search.py "screenshot testing compose" --domain testing-strategies

# Platform APIs
python scripts/search.py "camera permissions biometric" --domain platform-apis

# Build & Deploy
python scripts/search.py "play store fastlane" --domain build-deployment

# Stack-specific search
python scripts/search.py "room database" --stack kotlin
python scripts/search.py "swiftui navigation" --stack swift
python scripts/search.py "flutter bloc" --stack flutter
```

## Step 3: Apply Rules

Based on search output, apply:
1. Recommended architecture for the use case
2. Platform-specific implementation guidelines
3. Anti-patterns to avoid
4. Performance checklist

## Step 4: Generate Output

Always include:
- [ ] Architecture pattern with platform-specific implementation
- [ ] Navigation strategy
- [ ] State management approach
- [ ] Anti-patterns specific to the platform and use case
- [ ] Pre-delivery checklist (minimum 5 items)

## Output Format

```text
+--------------------------------------------------+
| TARGET: <project name>                           |
+--------------------------------------------------+
| PLATFORM:   <Android / iOS / KMM / Flutter>     |
| LANGUAGE:   <Kotlin / Swift / Dart>             |
| UI:         <Compose / SwiftUI / Flutter>       |
| ARCH:       <MVVM / MVI / Clean Architecture>   |
| NAVIGATION: <Stack + Tab + Deep Link>           |
| STATE:      <StateFlow / Combine / BLoC>        |
| DATABASE:   <Room / CoreData / SQLDelight>      |
| NETWORK:    <Retrofit / Ktor / Alamofire>       |
| DI:         <Hilt / Koin / Swinject>            |
| TESTING:    <Unit + UI + Screenshot>            |
| DEPLOY:     <Fastlane + Play/App Store>         |
| AVOID:      <anti-patterns for this context>    |
| CHECKLIST:  [ ] item 1                          |
|             [ ] item 2                          |
+--------------------------------------------------+
```

## Database Reference

- `data/ui_components.csv` — UI component patterns (14 rows)
- `data/navigation_patterns.csv` — Navigation strategies (12 rows)
- `data/architecture_patterns.csv` — Architecture patterns (12 rows)
- `data/state_management.csv` — State management approaches (12 rows)
- `data/performance_optimization.csv` — Performance rules (12 rows)
- `data/testing_strategies.csv` — Testing patterns (12 rows)
- `data/platform_apis.csv` — Platform API integration (12 rows)
- `data/build_deployment.csv` — Build and deployment automation (12 rows)
- `data/anti_patterns.csv` — Mobile anti-patterns (25+ rows)
- `data/stacks.csv` — Technology stacks including Kotlin, Swift, Flutter, KMM (24+ rows)
