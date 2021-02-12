<style>body {text-align: justify}</style>

# User Interface

## Main Window

**Main Window** is a face of Blender Launcher where all main features can be accessed.

The top horizontal menu bar contains following buttons from left to right:

1. Settings Menu
1. Documentation
1. Minimize to taskbar
1. Minimize to tray

**Main Window** layout consists of three main tabs with corresponding pages:

* **Library** - list of local builds ready to use
    * **Stable**
    * **Daily**
    * **Experimental**
* **Downloads** - list of available official builds
    * **Stable**
    * **Daily**
    * **Experimental**
* **User** - list of favorite and custom builds defined by user
    * **Favorites**
    * **Custom**

!!! tip

    Use ++"Scroll Wheel"++ while hovering tabs to quickly switch between them.

!!! note

    By default Library and Downloads pages will be automatically matched between each over. To change this behaviour toggle [Sync Library & Downloads Pages](settings.md#sync-library-downloads-pages) checkbox in settings.

The bottom status bar shows following information from left to right:

1. Status of application
1. Blender Launcher version number

## Library Tab

??? image "Screenshots"

    <figure>
      <img src="../imgs/library_daily.png"/>
      <figcaption>Library Tab, Daily Page</figcaption>
    </figure>

Library tab is a place where all local builds are shown based on category. Each category contains a list of items which represents a build information. Library build item shows following information from left to right:

1. Launch button

    !!! note

        Play icon :fontawesome-solid-play: on the right side of button indicates that build set to [quick launch](#add-to-quick-launch).

1. Version number including subversion or phase (Alpha, Beta)
1. Branch name
1. Date and time of build commit target

    !!! note

        Take in mind that [builder.blender.org](https://builder.blender.org/download/) shows when build was uploaded to server.

1. Number of running instances / new build indicator

!!! tip

    ++"2x Left Button"++ on library build item will automatically launch build.

### Library Build Context Menu

??? image "Screenshots"

    <figure>
      <img src="../imgs/library_context_menu.png"/>
      <figcaption>Library Build Context Menu</figcaption>
    </figure>

Build context menu can be accessed via right click on build item.

#### Add To Quick Launch

:   Sets selected build to be accessed from tray icon context menu or middle click on it.

#### Add To Favorites

:   Add selected build to Favorites page of User tab.

#### Register Extension [Windows only]

:   Silently register blend-file extension (show thumbnails in file explorer and use selected build as default to open `*.blend` files).

#### Create Shortcut

:   Create shortcut for selected build on desktop.

#### Create Symlink

:   Create [symbolic link](https://en.wikipedia.org/wiki/Symbolic_link) for selected build pointing to `%Library Folder%/blender_symlink`.

#### Show Folder

:   Reveal folder containing selected build in system file explorer.

#### Install Template

:   Install template for selected build (check [template](Library-Folder#template) for more details).

#### Delete From Drive

:   Delete selected build from drive and remove it from Blender Launcher.

## Downloads Tab

??? image "Screenshots"

    <figure>
      <img src="../imgs/downloads_experimental.png"/>
      <figcaption>Downloads Tab, Experimental Page</figcaption>
    </figure>

Downloads tab is a place where all available official builds are shown based on category. Each category contains a list of items which represents a build information. Downloadable build item shows following information from left to right:

1. Download button
1. Version number including subversion or phase (Alpha, Beta)
1. Branch name
1. Upload date and time of build to server
1. New build indicator

!!! tip

    ++"2x Left Button"++ on downloadable build item will automatically start downloading.

## User Tab

User tab is a place where favorite and custom builds can be defined.

### Favorites Page

??? image "Screenshots"

    <figure>
      <img src="../imgs/user_favorites.png"/>
      <figcaption>User Tab, Favorites Page</figcaption>
    </figure>

Favorites page contains builds added from Library tab using context menu `Add To Favorites` action. It has the same context menu as Library tab build item except possibility to rename branch title:

#### Rename Branch

:   Rename branch title (++return++ to submit new title, ++esc++ to reject editing).

### Custom Page

??? image "Screenshots"

    <figure>
      <img src="../imgs/user_custom.png"/>
      <figcaption>User Tab, Custom Page</figcaption>
    </figure>

Custom page contains builds that placed under [`custom`](library_folder.md#custom) directory of [`library folder`](library_folder.md). It acts the same way as the Library tab build item. After adding new builds inside `custom` folder make sure to press `Reload` button on the top right corner of page to force Blender Launcher read it from disk and show in list.
