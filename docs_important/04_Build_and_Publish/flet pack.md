# `flet pack`

Package a Flet application into a standalone desktop executable or app bundle using PyInstaller.

---

## Usage

```bash
flet pack [-h] [-v] [-i ICON] [-n NAME] [-D] [--distpath DISTPATH]
          [--add-data [ADD_DATA ...]] [--add-binary [ADD_BINARY ...]]
          [--hidden-import [HIDDEN_IMPORT ...]]
          [--product-name PRODUCT_NAME]
          [--file-description FILE_DESCRIPTION]
          [--product-version PRODUCT_VERSION]
          [--file-version FILE_VERSION] [--company-name COMPANY_NAME]
          [--copyright COPYRIGHT]
          [--codesign-identity CODESIGN_IDENTITY]
          [--bundle-id BUNDLE_ID] [--debug-console DEBUG_CONSOLE]
          [--uac-admin]
          [--pyinstaller-build-args [PYINSTALLER_BUILD_ARGS ...]]
          [-y]
          script

```

---

## Positional Arguments

### `script`

Path to the Python script that launches your Flet app.

* **Required:** True

---

## Options

### Build Configuration

* **`--add-binary`**
Additional binary files to be added to the executable.
* **Format:** `source:destination[:platform]`


* **`--add-data`**
Add additional non-binary files or folders to the bundle.
* **Format:** `source:destination`
* *Accepts one or more arguments.*


* **`--distpath`**
Directory where the packaged app will be placed.
* **Default:** `dist`


* **`--hidden-import`**
Add Python modules that are dynamically imported and not detected by static analysis.
* **`--onedir`** (Alias: `-D`)
Create a one-folder bundle instead of a single-file executable (**Windows only**).
* **`--pyinstaller-build-args`**
Additional raw arguments to the underlying PyInstaller build command.

### App Metadata & Branding

* **`--icon`** (Alias: `-i`)
Path to an icon file for your executable or app bundle.
* **Supported formats:** `.ico` (Windows), `.png` (Linux), and `.icns` (macOS).


* **`--name`** (Alias: `-n`)
Name for the generated executable (Windows) or app bundle (macOS).
* **`--product-name`**
Product name to be embedded in the executable (Windows) or bundle (macOS).
* **`--product-version`**
Product version for the executable (Windows) or bundle (macOS).
* **`--copyright`**
Copyright string embedded in the executable (Windows) or bundle (macOS).

### Windows Specific

* **`--company-name`**
Company name metadata for the Windows executable.
* **`--file-description`**
File description to embed in the executable.
* **`--file-version`**
File version for the executable in `n.n.n.n` format.
* **`--uac-admin`**
Request elevated (admin) permissions on application start. Adds a UAC manifest to the executable.

### macOS Specific

* **`--bundle-id`**
Bundle identifier used for macOS app packaging.
* **`--codesign-identity`**
Code signing identity to sign the app bundle.

### Debugging & Output

* **`--debug-console`**
Show python debug console window (ensure correct DEBUG level). Useful for troubleshooting runtime errors.
* **`--verbose`** (Alias: `-v`)
Enable verbose output. Use `-v` for standard verbose logging and `-vv` for more detailed output.
* **`--yes`** (Alias: `-y`)
Enable non-interactive mode. All prompts will be skipped.
* **`--help`** (Alias: `-h`)
Show the help message and exit.