# Troubleshooting

## First step

Before creating an issue, check following:
* Avoid duplicates - look through [open](https://github.com/DotBow/Blender-Launcher/issues) and [closed](https://github.com/DotBow/Blender-Launcher/issues?q=is%3Aissue+is%3Aclosed) issues sections and make sure problem is not reported by other user
* Make sure using the latest build of **Blender Launcher** from [releases section](https://github.com/DotBow/Blender-Launcher/releases)
* If **Blender 3D** is closing right after running it from **Blender Launcher** the problem is probably in build itself or in [configuration files](https://docs.blender.org/manual/en/2.83/advanced/blender_directory_layout.html)
* For general questions go to [Blender Artists thread](https://blenderartists.org/t/blender-launcher-standalone-software-client)
* On Linux it is possible to retrieve useful debug information using following command: \
`$ gdb ./Blender\ Launcher` \
`$ [...]` \
`$ run`

## How to report a bug

To report a bug, use an [issue template](https://github.com/DotBow/Blender-Launcher/issues/new?assignees=DotBow&labels=bug&template=bug_report.md&title=). Consider attaching a **BL.log** file if it exists near **Blender Launcher.exe**.
