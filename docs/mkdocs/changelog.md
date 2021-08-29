<style>body {text-align: justify}</style>

# Changelog

## 1.14.0 :fontawesome-solid-star:

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.14.0/Blender_Launcher_v1.14.0_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.14.0/Blender_Launcher_v1.14.0_Linux_x64.zip){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - On Linux scraper not filtering *.sha256 files [#89](https://github.com/DotBow/Blender-Launcher/issues/89)
    - Daily builds without branch info (stable) was broken
    - Link to the release notes was broken
    - When deleting builds button label was duplicated

    **New:**

    - Added `-debug` flag to retrieve additional useful debug information<br>
    Check [documentation](https://dotbow.github.io/Blender-Launcher/troubleshooting#catching-application-traceback) for how to use it
    - Blender 3.0 and higher on Windows now supports running via `blender-launcher.exe` without showing console at startup [#75](https://github.com/DotBow/Blender-Launcher/issues/75)<br>
    Activate `Hide Console On Startup` in settings to enable this feature
    - Build added to quick launch can be executed via global shortcut [#81](https://github.com/DotBow/Blender-Launcher/issues/81)<br>
    Activate `Quick Launch Global Shortcut` in settings to enable this feature
    - Windows taskbar thumbnail now has close and quick launch tool button
    - Show reload option for custom builds even if there is no any
    - Subversion indent now is constant

    **Known issues:**

    - When running Blender via `blender-launcher.exe` counting active instances isn't working

## 1.13.0

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.13.0/Blender_Launcher_v1.13.0_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.13.0/Blender_Launcher_v1.13.0_Linux_x64.zip){: .md-button .md-button--primary }

Follow [Installation](installation.md#installing-blender-launcher) and [Update](installation.md#updating-blender-launcher) instructions on [Documentation](https://dotbow.github.io/Blender-Launcher).<br>
Please, read about [how to report a bug](troubleshooting.md) before creating an issue.

??? summary "Release Notes"

    **Fixed:**

    - Site and naming convention changes broke proper build recognition and display [#70](https://github.com/DotBow/Blender-Launcher/issues/41)

    **New:**

    - Internal MacOS support (not builds yet)

    **Known issues:**

    - There is still might be some broken builds due to convention changes when migrating from 1.12.1 to 1.13.0 which should be removed manually from the Library Folder (folders named `blender-windows64`)

## 1.12.1

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.12.1/Blender_Launcher_v1.12.1_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.12.1/Blender_Launcher_v1.12.1_Linux_x64.zip){: .md-button .md-button--primary }

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

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.12.0/Blender_Launcher_v1.12.0_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.12.0/Blender_Launcher_v1.12.0_Linux_x64.zip){: .md-button .md-button--primary }

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

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.11.0/Blender_Launcher_v1.11.0_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.11.0/Blender_Launcher_v1.11.0_Linux_x64.zip){: .md-button .md-button--primary }

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

[:fontawesome-brands-windows: Windows x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.10.0/Blender_Launcher_v1.10.0_Windows_x64.zip){: .md-button .md-button--primary }
[:fontawesome-brands-linux: Linux x64](https://github.com/DotBow/Blender-Launcher/releases/download/v1.10.0/Blender_Launcher_v1.10.0_Linux_x64.zip){: .md-button .md-button--primary }

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
