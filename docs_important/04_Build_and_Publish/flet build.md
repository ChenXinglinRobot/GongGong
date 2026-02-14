# `flet build`

Build a Flet Python app into a platform-specific executable or installable bundle. It supports building for desktop (macOS, Linux, Windows), web, Android (APK/AAB), and iOS (IPA), with a wide range of customization options for metadata, assets, splash screens, and signing.

---

## Usage

```bash
flet build [-h] [-v] [-o OUTPUT_DIR]
           [--arch TARGET_ARCH [TARGET_ARCH ...]]
           [--exclude EXCLUDE [EXCLUDE ...]] [--clear-cache]
           [--project PROJECT_NAME] [--artifact ARTIFACT_NAME]
           [--description DESCRIPTION] [--product PRODUCT_NAME]
           [--org ORG_NAME] [--bundle-id BUNDLE_ID]
           [--company COMPANY_NAME] [--copyright COPYRIGHT]
           [--android-adaptive-icon-background ANDROID_ADAPTIVE_ICON_BACKGROUND]
           [--splash-color SPLASH_COLOR]
           [--splash-dark-color SPLASH_DARK_COLOR] [--no-web-splash]
           [--no-ios-splash] [--no-android-splash]
           [--ios-team-id IOS_TEAM_ID]
           [--ios-export-method IOS_EXPORT_METHOD]
           [--ios-provisioning-profile IOS_PROVISIONING_PROFILE]
           [--ios-signing-certificate IOS_SIGNING_CERTIFICATE]
           [--base-url BASE_URL]
           [--web-renderer {auto,canvaskit,skwasm}]
           [--route-url-strategy {path,hash}]
           [--pwa-background-color PWA_BACKGROUND_COLOR]
           [--pwa-theme-color PWA_THEME_COLOR] [--no-wasm] [--no-cdn]
           [--split-per-abi] [--compile-app] [--compile-packages]
           [--cleanup-app]
           [--cleanup-app-files [CLEANUP_APP_FILES ...]]
           [--cleanup-packages]
           [--cleanup-package-files [CLEANUP_PACKAGE_FILES ...]]
           [--flutter-build-args [FLUTTER_BUILD_ARGS ...]]
           [--source-packages SOURCE_PACKAGES [SOURCE_PACKAGES ...]]
           [--info-plist INFO_PLIST [INFO_PLIST ...]]
           [--macos-entitlements MACOS_ENTITLEMENTS [MACOS_ENTITLEMENTS ...]]
           [--android-features ANDROID_FEATURES [ANDROID_FEATURES ...]]
           [--android-permissions ANDROID_PERMISSIONS [ANDROID_PERMISSIONS ...]]
           [--android-meta-data ANDROID_META_DATA [ANDROID_META_DATA ...]]
           [--permissions {location,camera,microphone,photo_library} [{location,camera,microphone,photo_library} ...]]
           [--deep-linking-scheme DEEP_LINKING_SCHEME]
           [--deep-linking-host DEEP_LINKING_HOST]
           [--android-signing-key-store ANDROID_SIGNING_KEY_STORE]
           [--android-signing-key-store-password ANDROID_SIGNING_KEY_STORE_PASSWORD]
           [--android-signing-key-password ANDROID_SIGNING_KEY_PASSWORD]
           [--android-signing-key-alias ANDROID_SIGNING_KEY_ALIAS]
           [--build-number BUILD_NUMBER]
           [--build-version BUILD_VERSION]
           [--module-name MODULE_NAME] [--template TEMPLATE]
           [--template-dir TEMPLATE_DIR]
           [--template-ref TEMPLATE_REF] [--show-platform-matrix]
           [--no-rich-output] [--yes] [--skip-flutter-doctor]
           {macos,linux,windows,web,apk,aab,ipa} [python_app_path]

```

---

## Positional Arguments

### `target_platform`

The target platform or type of package to build.

* **Possible values:** `aab`, `apk`, `ipa`, `linux`, `macos`, `web`, `windows`
* **Required:** True

### `python_app_path`

Path to a directory with a Flet Python program.

* **Default:** `.` (Current directory)

---

## Options

### General & Metadata

* **`--project`**: Project name for bundle IDs and identifiers; used as the default for artifact and product names.
* **`--product`**: Display name shown in app launchers, window titles, and about dialogs.
* **`--description`**: Short description of the application.
* **`--org`**: Organization name in reverse domain name notation (e.g., `com.mycompany`), combined with project name and used in bundle IDs and signing.
* **`--company`**: Company name to display in about app dialogs.
* **`--copyright`**: Copyright text to display in about app dialogs.
* **`--bundle-id`**: Bundle ID for the application, e.g. `com.mycompany.app-name`. Used as an iOS, Android, macOS, and Linux bundle ID.
* **`--build-number`**: Build number - an integer used as an internal version number.
* **`--build-version`**: Build version - a `x.y.z` string used as the version number shown to users.

### Build Configuration & Output

* **`--output`** (Alias: `-o`): Output directory for the final executable/bundle (default: `/build/`).
* **`--artifact`**: Executable or bundle name on disk.
* **`--arch`**: Build for specific CPU architectures (used in macOS and Android builds only). Example: `--arch arm64 x64`.
* **`--compile-app`**: Pre-compile app's `.py` files to `.pyc`.
* **`--compile-packages`**: Pre-compile site packages' `.py` files to `.pyc`.
* **`--cleanup-app`**: Remove unnecessary app files upon packaging.
* **`--cleanup-app-files`**: The list of globs to delete extra app files and directories.
* **`--cleanup-packages`**: Remove unnecessary package files upon packaging.
* **`--cleanup-package-files`**: The list of globs to delete extra package files and directories.
* **`--clear-cache`**: Remove any existing build cache before starting the build process.
* **`--exclude`**: Files and/or directories to exclude from the package (can be used multiple times).
* **`--module-name`**: Python module name with an app entry point.
* **`--source-packages`**: The list of Python packages to install from source distributions.
* **`--template`**: Directory containing Flutter bootstrap template, or a URL to a git repository template.
* **`--template-dir`**: Relative path to a Flutter bootstrap template in a repository.
* **`--template-ref`**: The branch, tag, or commit ID to checkout after cloning the repository with Flutter bootstrap template.
* **`--flutter-build-args`**: Additional arguments for `flutter build` command.

### Android Specific

* **`--android-adaptive-icon-background`**: The color to be used to fill out the background of Android adaptive icons.
* **`--android-features`**: The list of `<feature_name>=True|False` features to add to `AndroidManifest.xml`.
* **`--android-meta-data`**: The list of `<name>=<value>` app meta-data entries to add to `AndroidManifest.xml`.
* **`--android-permissions`**: The list of `<permission_name>=True|False` permissions to add to `AndroidManifest.xml`.
* **`--split-per-abi`**: Split the APKs per ABIs.
* **`--no-android-splash`**: Disable splash screen on Android platform.
* **Signing:**
* `--android-signing-key-store`: Path to an upload keystore `.jks` file [env: `FLET_ANDROID_SIGNING_KEY_STORE`].
* `--android-signing-key-store-password`: Store password [env: `FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD`].
* `--android-signing-key-alias`: Key alias [env: `FLET_ANDROID_SIGNING_KEY_ALIAS`].
* `--android-signing-key-password`: Key password [env: `FLET_ANDROID_SIGNING_KEY_PASSWORD`].



### iOS Specific

* **`--ios-team-id`**: Apple developer team ID for signing iOS app bundle (ipa only).
* **`--ios-export-method`**: Export method for iOS app bundle (default: debugging).
* **`--ios-provisioning-profile`**: Provisioning profile name or UUID that should be used to sign and export iOS app bundle.
* **`--ios-signing-certificate`**: Signing certificate name, SHA-1 hash, or automatic selector to use for signing iOS app bundle.
* **`--no-ios-splash`**: Disable splash screen on iOS platform.

### Web Specific

* **`--base-url`**: Base URL from which the app is served.
* **`--web-renderer`**: Flutter web renderer to use [env: `FLET_WEB_RENDERER`]. Values: `auto`, `canvaskit`, `skwasm`.
* **`--route-url-strategy`**: Base URL path to serve the app from. Useful if the app is hosted in a subdirectory [env: `FLET_WEB_ROUTE_URL_STRATEGY`]. Values: `hash`, `path`.
* **`--pwa-background-color`**: Initial background color for your web app.
* **`--pwa-theme-color`**: Default color for your web app's user interface.
* **`--no-wasm`**: Disable WASM target for web build.
* **`--no-cdn`**: Disable loading of CanvasKit, Pyodide and fonts from CDN [env: `FLET_WEB_NO_CDN`].
* **`--no-web-splash`**: Disable splash screen on web platform.

### macOS Specific

* **`--info-plist`**: The list of `<key>=<value>|True|False` pairs to add to `Info.plist`.
* **`--macos-entitlements`**: The list of `<key>=<value>|True|False` entitlements for macOS builds.

### Permissions & Deep Linking

* **`--permissions`**: The list of pre-defined cross-platform permissions for iOS, Android and macOS builds.
* Possible values: `camera`, `location`, `microphone`, `photo_library`.


* **`--deep-linking-scheme`**: Deep linking URL scheme to configure for iOS and Android builds (e.g., `https` or `myapp`).
* **`--deep-linking-host`**: Deep linking URL host for iOS and Android builds.

### Splash Screen Appearance

* **`--splash-color`**: Background color of app splash screen on iOS, Android and web.
* **`--splash-dark-color`**: Background color in dark mode of app splash screen on iOS, Android and web.

### Flags & Diagnostics

* **`--verbose`** (Alias: `-v`): Enable verbose output (`-v` for standard, `-vv` for detailed).
* **`--yes`**: Answer yes to all prompts (install dependencies without confirmation).
* **`--help`** (Alias: `-h`): Show help message and exit.
* **`--show-platform-matrix`**: Display the build platform matrix in a table, then exit.
* **`--no-rich-output`**: Disable rich output and prefer plain text. Useful on Windows builds [env: `FLET_CLI_NO_RICH_OUTPUT`].
* **`--skip-flutter-doctor`**: Skip running Flutter doctor upon failed builds [env: `FLET_CLI_SKIP_FLUTTER_DOCTOR`].