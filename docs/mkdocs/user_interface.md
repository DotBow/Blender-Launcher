<style>body {text-align: justify}</style>

# User Interface

## Main Window

**Main Window** is a face of Blender Launcher where all main features can be accessed.

The top horizontal menu bar contains following buttons from left to right:

1. Settings Menu
1. Documentation
1. Minimize to taskbar
1. Minimize to tray

**Main Window** layout consists of three main tabs:

* **Library** - list of local builds ready to use
* **Downloads** - list of available official builds
* **User** - list of favorite and custom builds defined by user

The bottom status bar shows following information from left to right:

1. Status of application
1. Blender Launcher version number

## Library Tab

Library tab is a place where all local builds are shown based on category. Each category contains a list of items which represents a build information. Library build item shows following information from left to right:

1. Version number including subversion or phase (Alpha, Beta)
1. Branch name
1. Date and time of build commit target<br>
   Note: builder.blender.org shows when build was uploaded to server
1. Number of running instances
1. Favorite indicator

!!! tip

    ++"2x Left Button"++ on library build item will automatically launch build

## Library Build Context Menu

Build context menu can be accessed via right click on build item.

#### Add To Quick Launch
:   Sets selected build to be accessed from tray icon context menu or middle click on it.

#### Add To Favorites
:   Add selected build to Favorites page of User tab.

#### Register Extension [Windows only]
:   Silently register blend-file extension (show thumbnails in file explorer and use selected build as default to open ``*.blend`` files).

#### Create Shortcut
:   Create shortcut for selected build on desktop.

#### Create Symlink
:   Create [symbolic link](https://en.wikipedia.org/wiki/Symbolic_link) for selected build pointing to ``%Library Folder%/blender_symlink``.

#### Show Folder
:   Reveal folder containing selected build in system file explorer.

#### Install Template
:   Install template for selected build (check [template](Library-Folder#template) for more details).

#### Delete From Drive
:   Delete selected build from drive and remove it from Blender Launcher.

## Downloads Tab

Downloads tab is a place where all available official builds are shown based on category. \
Each category contains a list of items which represents a build information. \
Downloadable build item shows following information from left to right:

1. Version number
1. Branch name
1. Upload date and time of build to server
1. Commit hash number

!!! tip

    ++"2x Left Button"++ on downloadable build item will automatically start downloading

## User Tab
