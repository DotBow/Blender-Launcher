PYTHONOPTIMIZE=2 pyinstaller \
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
