PYTHONOPTIMIZE=2 /home/oleg/.local/bin/pyinstaller \
--clean \
--noconsole \
--noupx \
--onefile \
--windowed \
--icon="resources/icons/desktop.ico" \
--name="Blender Launcher" \
--version-file="version.txt" \
--add-binary="resources/icons/winblender.ico:files" \
main.py
