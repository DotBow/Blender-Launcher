<style>body {text-align: justify}</style>

# Changelog

## 1.11.0

[Download Blender Launcher v1.11.0 :fontawesome-solid-file-download:](https://github.com/DotBow/Blender-Launcher/releases/tag/v1.11.0){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - Fix release candidate title conversion to RC [unreported]
    - Custom page reload feature forces to draw all builds which leads to duplicates [unreported]
    - Fix crashing - library drawer and observer threads [unreported]
    - Fix alignment with 'RC' and 'Alpha' subversion labels [#56](https://github.com/DotBow/Blender-Launcher/issues/56)

    **New:**

    - Add animated icons to get back visualization of download and extract processes

    **Other:**

    - Move dialog creation into separate class, disable custom icons and set view to list by default

## 1.10.0

[Download Blender Launcher v1.10.0 :fontawesome-solid-file-download:](https://github.com/DotBow/Blender-Launcher/releases/tag/v1.10.0){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - Symlink doesn't work if associated folder was deleted
    - Small internal fixes and improvements

    **New:**

    - Refactored **Main Window** tabs and pages design
    - Refactored list design with better alignments matched between tabs and pages
    - Branch labels properly cropped when no enough space is available
    - Show build phase (Alpha, Beta) for daily builds in downloads tab
    - New **Favorites** tab that contains builds added from **Library** tab using context menu `Add To Favorites` action
    - Branch renaming support for **Favorites** tab
    - **Favorite** build renamed to **Quick Launch** and marks with play icon on the `Launch` button and `Blender` tray context menu action
    - New builds now marks with dot icon instead of "New" label
    - New option to disable tray icon and quit **Blender Launcher** on close
    - Context menus automatically positioned under first available option
    - Refactored automatic update system for better stability [#41](https://github.com/DotBow/Blender-Launcher/issues/41)

    **Other:**

    - **Wiki** was deprecated in favor of new [Documentation](https://dotbow.github.io/Blender-Launcher) site
    - Reading local builds now is more stable and fast
    - .blinfo file version update due to new **Favorites** tab - expect reloading all existing builds information at first start
    - **PyInstaller** version updated to 4.2
    - Added development packages to virtual environment
