# Settings

## Settings Window

To open the **Settings Window** use button with gear icon on top left of the **Main Window**.\
All changes saved automatically.

## Library Folder

**Library Folder** - a directory on hard drive, where all downloaded builds are stored. \
For detailed information check [Library Folder](wiki#Library-Folder) page.

## System

### Taskbar Icon Color

Determines the color of the **Blender Launcher** icon in taskbar so it is both readable in light and dark system themes. \
To apply changes application should be restarted.

### Launch When System Starts [Windows only]

Determines if **Blender Launcher** will run when system starts.

### Launch Minimized To Tray

Determines if **Main Window** will pop up when user execute **Blender Launcher** or only tray icon will be shown.

## Interface

### Default Library Page

Determines what page of Library tab will be opened when **Blender Launcher** starts.

### Default Downloads Page

Determines what page of Downloads tab will be opened when **Blender Launcher** starts.

### Enable High DPI Scaling

Determines if **Blender Launcher** user interface will automatically scale based on the monitor's pixel density. \
To apply changes application should be restarted.

## Notifications

### When New Builds Are Available

Show OS notifications when new new builds of Blender are available in Downloads tab.

### When Downloading Finished

Show OS notifications when build finished downloading and added to Library tab.

## New Build Actions

Actions that will be performed on newly added build to Library tab right after downloading is finished.

### Mark As Favorite

Mark every newly added build to Library tab as favorite depending on branch type.

### Install Template

Installs template on newly added build to Library tab.

## Blender Launching

### Startup Arguments

Adds specific instructions as if Blender was launching from the command line (after the blender executable i.e. ``blender [args …]``).<br/>
For example, adding ``-W`` (force opening Blender in fullscreen mode) argument internally will produce following command:

```
%path to blender executable% -W
```

List of commands can be found on Blender manual [Command Line Arguments](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html) page.

### Bash Arguments [Linux only]

Adds specific instructions as if Blender was launching from the command line (before the blender executable i.e. ``[args …] blender``).<br/>
For example, adding ``env __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia`` (force Blender to use dedicated graphics card) arguments internally will produce following command:

```
env __NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia nohup %path to blender executable% %startup arguments%
```