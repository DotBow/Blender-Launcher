# Library Folder

**Library Folder** - a directory on hard drive where all downloaded builds are stored.

!!! warning

    Don't create **Library Folder** inside UAC protected folders like **Program Files**. It is recommended to create a new directory on a non system drive or inside user folder like **Documents** to avoid any file collisions and have a nice structure.

## Structure

**Library Folder** has the following structure:

```
.
└─ %Library Folder%
    ├─ bl_symlink
    ├─ .temp
    ├─ custom
    ├─ daily
    ├─ experimental
    ├─ stable
    └─ template
```

### bl_symlink

**bl_symlink** is a symbolic link that creates via [library build context menu](User-Interface#library-build-context-menu).

### .temp

**.temp** folder is used to store downloaded *.zip and *.tar files.

### custom

**custom** folder is used to store builds downloaded by user manually (e.g. from [GraphicAll](https://blender.community/c/graphicall/)). \
To use custom builds with Blender Launcher they must be placed inside **custom** folder manually:

```
.
└─ %Library Folder%
    └─ custom
        ├─ %custom blender build 1%
        │   ├─ ...
        │   ├─ blender.exe
        │   └─ ...
        ├─ %custom blender build 2%
        │   ├─ ...
        │   ├─ blender.exe
        │   └─ ...
        └─ ...
```

### daily

**daily** folder is used to store [daily builds](https://builder.blender.org/download/).

### experimental

**experimental** folder is used to store [experimental branches builds](https://builder.blender.org/download/branches/).

### stable

**stable** folder is used to store [stable builds](https://download.blender.org/release/).

### template

**template** folder is used to store custom Blender preferences and scripts (e.g. [HEAVYPOLY config](https://github.com/HEAVYPOLY/HEAVYPOLY_Blender)).<br/>
Template represents a file structure similar to one existing in Blender build (e.g. ``blender-2.91.0-windows64\2.91``):

```
.
└─ %Library Folder%
    └─ template
        ├─ ...
        ├─ config
        ├─ datafiles
        ├─ scripts
        │   ├─ ...
        │   ├─ addons
        │   ├─ startup
        │   └─ ...
        └─...
```
