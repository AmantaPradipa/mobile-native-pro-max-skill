# Use Case: E-Commerce Android App

## Request
"Build an e-commerce app for Android using Kotlin and Jetpack Compose"

## Search Command
```bash
python scripts/search.py "e-commerce android kotlin compose" --architecture -p "ShopApp"
```

## Expected Output
```
TARGET: ShopApp
PLATFORM:   Android
LANGUAGE:   Kotlin
UI:         Jetpack Compose + Material 3
ARCH:       MVVM + Clean Architecture + Multi-Module
NAVIGATION: Stack (product detail) + Tab (home/cart/profile) + Deep Link (product share)
STATE:      StateFlow + sealed class UiState
DATABASE:   Room with DiffUtil
NETWORK:    Retrofit + OkHttp + Moshi
DI:         Hilt
TESTING:    Unit (MockK + Turbine) + UI (Compose Test) + Screenshot (Paparazzi)
DEPLOY:     Fastlane + Play Console internal track
AVOID:      Main-thread network, God Activity, Missing ProGuard
```
