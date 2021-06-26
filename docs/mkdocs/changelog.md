<style>body {text-align: justify}</style>

# Changelog

## 1.12.1

[Download Blender Launcher v1.12.1 :fontawesome-solid-file-download:](https://github.com/DotBow/Blender-Launcher/releases/tag/v1.12.1){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - Daily and Experimental builds messed up after massive site changes [#65](https://github.com/DotBow/Blender-Launcher/issues/65)

    **Other:**

    - Minimum GLIBC version raised to 2.31
    - Python version updated to 3.9

    **Known issues:**

    - New naming conventions may break branch labels for experimental builds


## 1.12.0

[Download Blender Launcher v1.12.0 :fontawesome-solid-file-download:](https://github.com/DotBow/Blender-Launcher/releases/tag/v1.12.0){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - Subversion label doesn't fit five-digit version numbers [#62](https://github.com/DotBow/Blender-Launcher/issues/62)
    - Select only active widget when launching build
    - Runtime error when application terminates on update or when `Show Tray Icon` option is disabled

    **New:**

    - Added `Show Release Notes` context menu action for Stable and LTS builds to reveal page with release notes for selected build in web browser
    - Hash number display can be accessed by clicking on **Commit Time**/**Upload Time** label of build item
    - **Library Folder** now can be set via command line arguments [#52](https://github.com/DotBow/Blender-Launcher/issues/52)<br>
    Read about how to use it on [Changing Library Folder](library_folder.md#changing-library-folder) section
    - BL will warn the user when different version of the application is launched [#44](https://github.com/DotBow/Blender-Launcher/issues/44)

    **Other:**

    - Multiple builds deletion stability improvements
    - PyInstaller version updated to 4.3 [Windows]
    - UI polishing

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
