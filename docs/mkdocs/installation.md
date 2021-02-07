# Installation

## Installing Blender Launcher

1. Download latest release for your OS from [releases page](https://github.com/DotBow/Blender-Launcher/releases/latest)
1. Unpack ``Blender Launcher.exe`` file and place it somewhere on your drive
1. Run ``Blender Launcher.exe`` file
1. If this is a first launch, program will ask for choosing [Library Folder](library_folder.md)
1. Enjoy!

## Updating Blender Launcher

### Manual update

1. Download latest release for your OS from [releases page](https://github.com/DotBow/Blender-Launcher/releases/latest)
1. Quit running instance of **Blender Launcher**
1. Unpack ``Blender Launcher.exe`` file and replace existing one
1. Enjoy!

### Automatic update

1. Press the ``Update to version %.%.%`` button on the right bottom corner
1. Wait until downloading and extracting process is finished
1. Wait for ~5-30 second while new version is configured and automatically launched
1. Enjoy!

## Important Notes

!!! warning "Library Folder"

    It is recommended to create a new folder on a non system drive or inside user folder like ``Documents`` to avoid any file collisions and have a nice structure.

!!! warning "Windows Users"

    Don't use UAC protected folders like ``Program Files`` and don't run **Blender Launcher** with administration rights. It may cause unexpected behavior for program itself as well as Blender 3D.

!!! info "Linux Users"

    - Make sure that OS GLIBC version is 2.27 or higher otherwise try to build **Blender Launcher** from source manually following [Development](https://github.com/DotBow/Blender-Launcher/wiki/Development) Wiki page.
    - Consider installing [TopIcons Plus](https://extensions.gnome.org/extension/1031/topicons/) extension for proper tray icon support.

!!! info "Blender Version Manager Users"

    Since **Blender Launcher** is written from scratch with a different concept in mind it is strongly recommended not to use a **Root Folder** as **Library Folder**. Otherwise delete all builds from **Root Folder** or move them to ``%Library Folder%\daily`` directory.
